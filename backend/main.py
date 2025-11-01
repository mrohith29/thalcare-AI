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
