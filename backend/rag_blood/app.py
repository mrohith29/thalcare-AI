# app.py
import os, math, time, json, hashlib, pathlib
from typing import Optional, List

import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

# ---------- ENV ----------
DATA_PATH = os.environ.get("DATA_PATH", "./data/blood_request_ranking_dataset_with_coords.csv")
EMBED_MODEL_NAME = os.environ.get("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
CROSS_ENCODER_NAME = os.environ.get("CROSS_ENCODER", "cross-encoder/ms-marco-MiniLM-L-6-v2")
CHROMA_DIR = os.environ.get("CHROMA_DIR", "./chroma_hospitals")
TOP_K_RETRIEVE = int(os.environ.get("TOP_K_RETRIEVE", "200"))  # a bit wider to find more same-city hits
TOP_N_RETURN = int(os.environ.get("TOP_N_RETURN", "10"))
CITY_PRIORITY_WEIGHT = float(os.environ.get("CITY_PRIORITY_WEIGHT", "0.35"))  # boost for same-city
DISTANCE_PENALTY_WEIGHT = float(os.environ.get("DISTANCE_PENALTY_WEIGHT", "0.10"))  # gentler distance penalty

os.makedirs(CHROMA_DIR, exist_ok=True)

from sentence_transformers import SentenceTransformer, CrossEncoder
import chromadb
from chromadb.config import Settings

# ---------- Helpers ----------
def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0088
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2)**2 +
         math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlon/2)**2)
    return 2 * R * math.asin(math.sqrt(a))

def to_bool(x):
    if isinstance(x, bool): return x
    if isinstance(x, (int, float)): return bool(int(x))
    if isinstance(x, str): return x.strip().lower() in {"1","true","yes","y"}
    return False

def s(x):  # safe string
    return "" if pd.isna(x) else str(x)

def file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1_048_576), b""):
            h.update(chunk)
    return h.hexdigest()

# ---------- Load dataset ----------
df = pd.read_csv(DATA_PATH)
if "Hospital_ID" not in df.columns:
    raise RuntimeError("CSV must contain Hospital_ID")

if "Request_Timestamp" in df.columns:
    tmp = df.copy()
    tmp["__ts"] = pd.to_datetime(tmp["Request_Timestamp"], errors="coerce", dayfirst=True)
    tmp = tmp.sort_values(["Hospital_ID", "__ts"], ascending=[True, False])
    hospitals = tmp.drop_duplicates(subset=["Hospital_ID"], keep="first").copy()
else:
    hospitals = df.drop_duplicates(subset=["Hospital_ID"], keep="first").copy()

OPTIONAL_BOOL = ["Emergency_Service", "24x7_Availability"]
OPTIONAL_NUM = [
    "Beds_Available", "Doctors_On_Duty", "Units_Available",
    "Patient_Satisfaction_%", "Blood_Safety_Score_%",
    "Avg_Response_Time_Min", "Last_Updated_Min_Ago",
    "Hospital_Latitude", "Hospital_Longitude",
]
OPTIONAL_TXT = [
    "Hospital_Name", "District", "City", "State",
    "Blood_Group_Available", "Component_Available",
    "Blood_Bank_Level"
]
for col in OPTIONAL_BOOL + OPTIONAL_NUM + OPTIONAL_TXT:
    if col not in hospitals.columns:
        hospitals.loc[:, col] = np.nan

for b in OPTIONAL_BOOL:
    hospitals.loc[:, b] = hospitals[b].apply(to_bool)
for n in OPTIONAL_NUM:
    hospitals.loc[:, n] = pd.to_numeric(hospitals[n], errors="coerce")

def row_to_profile(r):
    bullets = [f"Hospital: {s(r.get('Hospital_Name'))}"]
    loc_bits = []
    if not pd.isna(r.get("District")): loc_bits.append(f"District: {s(r.get('District'))}")
    if not pd.isna(r.get("City")): loc_bits.append(f"City: {s(r.get('City'))}")
    if not pd.isna(r.get("State")): loc_bits.append(f"State: {s(r.get('State'))}")
    if loc_bits: bullets.append(", ".join(loc_bits))
    if not pd.isna(r.get("Blood_Group_Available")):
        bullets.append(f"Blood groups: {s(r.get('Blood_Group_Available'))}")
    if not pd.isna(r.get("Component_Available")):
        bullets.append(f"Components: {s(r.get('Component_Available'))}")
    if not pd.isna(r.get("Units_Available")):
        bullets.append(f"Units available: {s(r.get('Units_Available'))}")
    if not pd.isna(r.get("Blood_Bank_Level")):
        bullets.append(f"Blood bank level: {s(r.get('Blood_Bank_Level'))}")
    bullets.append(f"Emergency: {bool(r.get('Emergency_Service', False))}; 24x7: {bool(r.get('24x7_Availability', False))}")
    if not pd.isna(r.get("Beds_Available")) or not pd.isna(r.get("Doctors_On_Duty")):
        bullets.append(f"Beds: {s(r.get('Beds_Available'))}; Doctors on duty: {s(r.get('Doctors_On_Duty'))}")
    if not pd.isna(r.get("Patient_Satisfaction_%")) or not pd.isna(r.get("Blood_Safety_Score_%")):
        bullets.append(f"Patient satisfaction: {s(r.get('Patient_Satisfaction_%'))}%; Safety score: {s(r.get('Blood_Safety_Score_%'))}%")
    if not pd.isna(r.get("Avg_Response_Time_Min")):
        bullets.append(f"Avg response time (min): {s(r.get('Avg_Response_Time_Min'))}")
    return " | ".join([b for b in bullets if b])

hospitals.loc[:, "profile_text"] = hospitals.apply(row_to_profile, axis=1)

# ---------- Models + Chroma (auto-rebuild if data changed) ----------
embedder = SentenceTransformer(EMBED_MODEL_NAME)
cross_encoder = CrossEncoder(CROSS_ENCODER_NAME)

client = chromadb.PersistentClient(path=CHROMA_DIR, settings=Settings(anonymized_telemetry=False))
INDEX_FINGERPRINT_PATH = os.path.join(CHROMA_DIR, "dataset_fingerprint.json")
current_fp = {"data_path": os.path.abspath(DATA_PATH), "sha256": file_sha256(DATA_PATH)}
prev_fp = None
if os.path.exists(INDEX_FINGERPRINT_PATH):
    try:
        prev_fp = json.loads(pathlib.Path(INDEX_FINGERPRINT_PATH).read_text())
    except Exception:
        prev_fp = None
need_rebuild = (prev_fp != current_fp)

if need_rebuild:
    try:
        for c in client.list_collections():
            client.delete_collection(c.name)
    except Exception:
        pass

coll_names = [c.name for c in client.list_collections()]
coll = client.get_collection("hospitals") if "hospitals" in coll_names else client.create_collection("hospitals")

if need_rebuild or coll.count() == 0:
    docs = hospitals["profile_text"].tolist()
    ids = hospitals["Hospital_ID"].astype(str).tolist()
    meta_cols = [c for c in [
        "Hospital_ID","Hospital_Name","District","City","State",
        "Hospital_Latitude","Hospital_Longitude",
        "Blood_Group_Available","Component_Available","Units_Available",
        "Emergency_Service","24x7_Availability",
        "Beds_Available","Doctors_On_Duty",
        "Patient_Satisfaction_%","Blood_Safety_Score_%",
        "Avg_Response_Time_Min","Last_Updated_Min_Ago"
    ] if c in hospitals.columns]
    metadatas = hospitals[meta_cols].to_dict(orient="records")
    embeddings = embedder.encode(docs, show_progress_bar=True, normalize_embeddings=True)
    coll.add(documents=docs, ids=ids, metadatas=metadatas, embeddings=embeddings)
    pathlib.Path(INDEX_FINGERPRINT_PATH).write_text(json.dumps(current_fp))

# ---------- API schema ----------
class SuggestRequest(BaseModel):
    blood_group: str
    component: str
    units_needed: int = Field(..., ge=1)
    urgency: str

    # City-first prioritization
    user_city: Optional[str] = None  # <- NEW

    # Optional geo filtering (kept optional now)
    user_lat: Optional[float] = None
    user_lon: Optional[float] = None
    within_km: Optional[float] = None  # <- default None means DO NOT filter by radius

    # Optional additional filters
    district: Optional[str] = None
    require_24x7: Optional[bool] = False
    require_emergency_service: Optional[bool] = False

    # Ranking + results
    top_n: int = Field(TOP_N_RETURN, ge=1, le=50)
    rerank: bool = True

    # Auto-expand (only used if within_km is set)
    expand_radius_if_few: bool = True
    min_results: int = 5

class Suggestion(BaseModel):
    hospital_id: str
    hospital_name: str
    district: Optional[str]
    city: Optional[str]
    state: Optional[str]
    distance_km: Optional[float] = None
    score: float
    reasons: List[str]

class SuggestResponse(BaseModel):
    took_ms: int
    query_used: str
    results: List[Suggestion]

app = FastAPI(title="Blood RAG + Rerank (City-first)")

# ---------- Retrieval / Filters ----------
def build_query_text(p: SuggestRequest) -> str:
    parts = [
        f"Need {p.units_needed} units of {p.blood_group}",
        f"component {p.component}",
        f"urgency {p.urgency}",
    ]
    if p.require_24x7: parts.append("24x7 availability required")
    if p.require_emergency_service: parts.append("emergency service required")
    if p.user_city: parts.append(f"prefer city {p.user_city}")
    if p.district: parts.append(f"prefer district {p.district}")
    if p.user_lat is not None and p.user_lon is not None and p.within_km:
        parts.append(f"within {p.within_km} km")
    return ", ".join(parts)

def hard_filter(meta: dict, req: SuggestRequest) -> bool:
    if req.require_24x7 and not to_bool(meta.get("24x7_Availability", False)):
        return False
    if req.require_emergency_service and not to_bool(meta.get("Emergency_Service", False)):
        return False

    bg_ok = True
    comp_ok = True
    units_ok = True

    if isinstance(meta.get("Blood_Group_Available"), str):
        avail_bgs = [x.strip() for x in str(meta["Blood_Group_Available"]).replace(" ", "").split(",") if x]
        bg_ok = (req.blood_group in avail_bgs)
    if isinstance(meta.get("Component_Available"), str):
        avail_comp = [x.strip().lower() for x in str(meta["Component_Available"]).replace(" ", "").split(",") if x]
        comp_ok = (req.component.lower() in avail_comp)
    if meta.get("Units_Available") is not None and str(meta.get("Units_Available")) != "nan":
        try: units_ok = float(meta["Units_Available"]) >= req.units_needed
        except: units_ok = True

    return bg_ok and comp_ok and units_ok

def compute_distance(meta: dict, req: SuggestRequest) -> Optional[float]:
    if req.user_lat is None or req.user_lon is None:
        return None
    lat = meta.get("Hospital_Latitude"); lon = meta.get("Hospital_Longitude")
    try:
        return haversine_km(float(req.user_lat), float(req.user_lon), float(lat), float(lon))
    except Exception:
        return None

def reasons(meta: dict, distance: Optional[float]):
    r = []
    if to_bool(meta.get("Emergency_Service", False)): r.append("Emergency services available")
    if to_bool(meta.get("24x7_Availability", False)): r.append("Open 24x7")
    if meta.get("Blood_Safety_Score_%") and not pd.isna(meta.get("Blood_Safety_Score_%")):
        try: r.append(f"Safety score {int(float(meta['Blood_Safety_Score_%']))}%")
        except: pass
    if meta.get("Patient_Satisfaction_%") and not pd.isna(meta.get("Patient_Satisfaction_%")):
        try: r.append(f"Patient satisfaction {int(float(meta['Patient_Satisfaction_%']))}%")
        except: pass
    if meta.get("Avg_Response_Time_Min") and not pd.isna(meta.get("Avg_Response_Time_Min")):
        try: r.append(f"Avg response time {int(float(meta['Avg_Response_Time_Min']))} min")
        except: pass
    if meta.get("Units_Available") and not pd.isna(meta.get("Units_Available")):
        try: r.append(f"Units available {int(float(meta['Units_Available']))}")
        except: pass
    if meta.get("Beds_Available") and not pd.isna(meta.get("Beds_Available")):
        try: r.append(f"Beds {int(float(meta['Beds_Available']))}")
        except: pass
    if distance is not None:
        r.append(f"~{round(distance,1)} km away")
    return r[:5]

# ---------- Endpoint ----------
@app.post("/suggest", response_model=SuggestResponse)
def suggest(req: SuggestRequest):
    t0 = time.time()
    # At least one of these should be present to personalize:
    if not (req.user_city or (req.user_lat is not None and req.user_lon is not None) or req.district):
        raise HTTPException(status_code=400, detail="Provide user_city or (user_lat & user_lon) or district.")

    query_text = build_query_text(req)
    q_emb = embedder.encode([query_text], normalize_embeddings=True)
    out = coll.query(
        query_embeddings=q_emb.tolist(),
        n_results=TOP_K_RETRIEVE,
        include=["documents", "metadatas", "distances"]
    )
    ids, metas, docs = out["ids"][0], out["metadatas"][0], out["documents"][0]

    # Build candidate pool; DO NOT radius-filter unless within_km provided.
    candidates = []
    for _id, meta, doc in zip(ids, metas, docs):
        if req.district and meta.get("District"):
            if str(meta.get("District","")).strip().lower() != req.district.strip().lower():
                # not same district: still allow; city-first ranking will handle priority
                pass

        if not hard_filter(meta, req):
            continue

        dist_km = compute_distance(meta, req)

        # Strict radius ONLY if within_km specified
        if req.within_km is not None and dist_km is not None and dist_km > req.within_km:
            continue

        candidates.append({
            "id": str(meta.get("Hospital_ID")),
            "name": meta.get("Hospital_Name"),
            "district": meta.get("District"),
            "city": meta.get("City"),
            "state": meta.get("State"),
            "distance_km": dist_km,
            "meta": meta,
            "profile": doc
        })

    if not candidates:
        raise HTTPException(status_code=404, detail="No matching hospitals after filters.")

    # City-first ordering (pre-rank): same-city first
    if req.user_city:
        same_city = [c for c in candidates if (c["city"] or "").strip().lower() == req.user_city.strip().lower()]
        other_city = [c for c in candidates if c not in same_city]
        candidates = same_city + other_city

    # Cross-encoder rerank
    if req.rerank:
        pairs = []
        for h in candidates:
            bits = [
                f"blood_group={req.blood_group}",
                f"component={req.component}",
                f"units_needed={req.units_needed}",
                f"urgency={req.urgency}",
            ]
            if req.require_24x7: bits.append("need_24x7=True")
            if req.require_emergency_service: bits.append("need_emergency=True")
            if req.user_city: bits.append(f"user_city={req.user_city}")
            if h["city"]: bits.append(f"hospital_city={h['city']}")
            user_need = " | ".join(bits)
            pairs.append((f"User need: {user_need}", f"Hospital profile: {h['profile']}"))
        ce_scores = CrossEncoder(CROSS_ENCODER_NAME).predict(pairs).tolist()
    else:
        ce_scores = [0.0] * len(candidates)

    # Final blend with city priority + gentle distance penalty
    blended = []
    for h, s in zip(candidates, ce_scores):
        m = h["meta"]
        safety = float(m.get("Blood_Safety_Score_%") or 0) / 100.0
        sats = float(m.get("Patient_Satisfaction_%") or 0) / 100.0
        resp = float(m.get("Avg_Response_Time_Min") or 30.0)
        beds = float(m.get("Beds_Available") or 0)
        docs_on = float(m.get("Doctors_On_Duty") or 0)

        # city match boost
        city_match = 1.0 if (req.user_city and (h["city"] or "").strip().lower() == req.user_city.strip().lower()) else 0.0

        # distance penalty (gentle; only if distance known)
        dist_pen = 0.0
        if h["distance_km"] is not None:
            over = max(0.0, h["distance_km"] - 5.0)
            dist_pen = over / 20.0  # slower penalty slope

        composite = (
            0.55 * s +
            0.10 * safety +
            0.10 * sats +
            0.08 * min(beds/50.0, 1.0) +
            0.05 * min(docs_on/10.0, 1.0) +
            0.07 * (1.0 - min(resp/60.0, 1.0)) +
            CITY_PRIORITY_WEIGHT * city_match -
            DISTANCE_PENALTY_WEIGHT * dist_pen
        )
        blended.append((composite, h))

    blended.sort(key=lambda x: x[0], reverse=True)
    top = blended[: req.top_n]

    results = []
    for sc, h in top:
        m = h["meta"]
        results.append(Suggestion(
            hospital_id=h["id"],
            hospital_name=h["name"],
            district=h.get("district"),
            city=h.get("city"),
            state=h.get("state"),
            distance_km=None if h["distance_km"] is None else round(h["distance_km"], 2),
            score=float(round(sc, 4)),
            reasons=reasons(m, h["distance_km"])
        ))

    return SuggestResponse(
        took_ms=int((time.time() - t0) * 1000),
        query_used=query_text,
        results=results
    )

# ---------- Friendly pages ----------
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h2>Blood RAG + Rerank — City-first</h2>
    <p>Use <a href="/docs">/docs</a> to try <code>POST /suggest</code>.</p>
    <p>Send <code>user_city</code> to prioritize hospitals in that city.
       Distance filtering is optional; set <code>within_km</code> if desired.</p>
    <p>Tune boosts via env: <code>CITY_PRIORITY_WEIGHT</code>, <code>DISTANCE_PENALTY_WEIGHT</code>.</p>
    """

@app.get("/healthz")
def health():
    return {"ok": True}
