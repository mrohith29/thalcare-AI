<<<<<<< HEAD
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
import uvicorn

app = FastAPI(
    title="Thalcare AI API",
    description="API for Thalcare AI - Blood Donation Network",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/api", tags=["api"])

@app.get("/")
def root():
    return {"message": "Welcome to Thalcare AI API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    
=======
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import crud, schemas
from database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/signup/patient")
def signup_patient(user: schemas.UserCreate, patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user, patient, role="patient")

@app.post("/signup/donor")
def signup_donor(user: schemas.UserCreate, donor: schemas.DonorCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user, donor, role="donor")

@app.post("/signup/hospital")
def signup_hospital(user: schemas.UserCreate, hospital: schemas.HospitalCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user, hospital, role="hospital")

# GET APIs
@app.get("/patients/view_donors")
def get_donors(db: Session = Depends(get_db)):
    return db.query(crud.Donor).all()

@app.get("/patients/view_hospitals")
def get_hospitals(db: Session = Depends(get_db)):
    return db.query(crud.Hospital).all()

@app.get("/donors/view_patients")
def get_patients(db: Session = Depends(get_db)):
    return db.query(crud.Patient).all()

@app.get("/donors/view_hospitals")
def get_hospitals(db: Session = Depends(get_db)):
    return db.query(crud.Hospital).all()

@app.get("/hospitals/view_donors")
def get_donors(db: Session = Depends(get_db)):
    return db.query(crud.Donor).all()
>>>>>>> 081fbde (main.py)
