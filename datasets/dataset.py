# Generate diversified synthetic dataset (~1100 records) based on the sample structure.
import random
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import numpy as np
rand = np.random.default_rng(42)

input_path = Path("sample_blood_banks.xlsx")
df_sample = pd.read_excel(input_path)

# Use sample columns as template
cols = df_sample.columns.tolist()

# City-State-LatLon samples across many Indian states (diverse)
city_state_coords = [
    ("Mumbai","Maharashtra",19.0760,72.8777),
    ("Pune","Maharashtra",18.5204,73.8567),
    ("Nagpur","Maharashtra",21.1458,79.0882),
    ("Delhi","Delhi",28.7041,77.1025),
    ("New Delhi","Delhi",28.6139,77.2090),
    ("Bengaluru","Karnataka",12.9716,77.5946),
    ("Mysore","Karnataka",12.2958,76.6394),
    ("Chennai","Tamil Nadu",13.0827,80.2707),
    ("Coimbatore","Tamil Nadu",11.0168,76.9558),
    ("Hyderabad","Telangana",17.3850,78.4867),
    ("Secunderabad","Telangana",17.4399,78.4983),
    ("Kolkata","West Bengal",22.5726,88.3639),
    ("Howrah","West Bengal",22.5958,88.2636),
    ("Visakhapatnam","Andhra Pradesh",17.6868,83.2185),
    ("Vijayawada","Andhra Pradesh",16.5062,80.6480),
    ("Bhopal","Madhya Pradesh",23.2599,77.4126),
    ("Indore","Madhya Pradesh",22.7196,75.8577),
    ("Jaipur","Rajasthan",26.9124,75.7873),
    ("Jodhpur","Rajasthan",26.2389,73.0243),
    ("Ahmedabad","Gujarat",23.0225,72.5714),
    ("Surat","Gujarat",21.1702,72.8311),
    ("Lucknow","Uttar Pradesh",26.8467,80.9462),
    ("Kanpur","Uttar Pradesh",26.4499,80.3319),
    ("Varanasi","Uttar Pradesh",25.3176,82.9739),
    ("Patna","Bihar",25.5941,85.1376),
    ("Ranchi","Jharkhand",23.3441,85.3096),
    ("Bhubaneswar","Odisha",20.2961,85.8245),
    ("Thiruvananthapuram","Kerala",8.5241,76.9366),
    ("Kochi","Kerala",9.9312,76.2673),
    ("Guwahati","Assam",26.1445,91.7362),
    ("Imphal","Manipur",24.8170,93.9368),
    ("Shillong","Meghalaya",25.5788,91.8933),
    ("Panaji","Goa",15.4909,73.8278),
    ("Chandigarh","Chandigarh",30.7333,76.7794),
    ("Dehradun","Uttarakhand",30.3165,78.0322),
    ("Shimla","Himachal Pradesh",31.1048,77.1734),
    ("Raipur","Chhattisgarh",21.2514,81.6296),
    ("Agartala","Tripura",23.8315,91.2868),
    ("Aizawl","Mizoram",23.7271,92.7176),
    ("Kohima","Nagaland",25.6740,94.1100)
]

blood_groups = ["A+","A-","B+","B-","O+","O-","AB+","AB-"]
hospital_types = ["Private","Government","Trust","Charity"]
names_prefix = ["Global","City","Central","Metro","Life","Care","Royal","National","Red Cross","Unity","St. Mary","Gandhi","Apollo","Fortis","Max","KIMS","Sankara"]

n = 1100  # chosen within requested 1000-1200
records = []
start_id = 1

for i in range(n):
    cid = f"BB{start_id+i:04d}"
    city, state, lat, lon = random.choice(city_state_coords)
    name = f"{random.choice(names_prefix)} {city} Blood Bank"
    lic_year = random.randint(2018,2024)
    lic_num = f"{state[:2].upper()}/BB/{lic_year}/{rand.integers(10,999):03d}"
    # License valid till: random future/past date within 2024-2030
    valid_till = datetime(rand.integers(2024,2031), rand.integers(1,13), rand.integers(1,28)+1).date()
    hospital_type = random.choices(hospital_types, weights=[0.55,0.25,0.12,0.08])[0]
    bg = random.choice(blood_groups)
    # Ensure ample of rarer groups by boosting probability occasionally
    if rand.random() < 0.05:
        bg = random.choice(["AB-","B-","A-","O-"])
    units = int(abs(rand.normal(20,12)))  # many around 20, but variability
    # cap units
    units = max(0, min(units, 120))
    freshness = int(rand.integers(0,8))  # days since collection
    emergency = random.choices(["Yes","No"], weights=[0.65,0.35])[0]
    rating = round(max(2.0, min(5.0, rand.normal(4.2,0.5))),1)
    distance = round(float(abs(rand.normal(8,12))),1)
    response_time = int(max(2, min(240, int(abs(rand.normal(25,20))))))
    is_govt = 1 if hospital_type=="Government" else 0
    contact = f"+91-{rand.integers(600000000,999999999)}"
    record = {
        "BloodBank_ID": cid,
        "BloodBank_Name": name,
        "License_Number": lic_num,
        "License_Valid_Till": valid_till.isoformat(),
        "State": state,
        "City": city,
        "Latitude": round(lat + rand.normal(0,0.05),6),
        "Longitude": round(lon + rand.normal(0,0.05),6),
        "Hospital_Type": hospital_type,
        "Blood_Group": bg,
        "Units_Available": units,
        "Freshness_Days": freshness,
        "Emergency_Support": emergency,
        "Rating": rating,
        "Distance_km": distance,
        "Avg_Response_Time_min": response_time,
        "Is_Govt": is_govt,
        "Contact": contact
    }
    records.append(record)

df_new = pd.DataFrame(records, columns=[
    "BloodBank_ID","BloodBank_Name","License_Number","License_Valid_Till","State","City",
    "Latitude","Longitude","Hospital_Type","Blood_Group","Units_Available","Freshness_Days",
    "Emergency_Support","Rating","Distance_km","Avg_Response_Time_min","Is_Govt","Contact"
])

# Quick checks: distribution counts for blood groups and states (top 10)
bg_counts = df_new["Blood_Group"].value_counts().sort_index()
state_counts = df_new["State"].value_counts().nlargest(15)

# Save files
out_csv = Path("synthetic_blood_banks_1100.csv")
out_xlsx = Path("synthetic_blood_banks_1100.xlsx")
df_new.to_csv(out_csv, index=False)
df_new.to_excel(out_xlsx, index=False)

# Display a preview and the distributions
df_preview = df_new.head(10)
bg_counts, state_counts, df_preview.to_dict(orient='records')[:5], str(out_csv), str(out_xlsx)
