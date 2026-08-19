from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine
from app.schemas.appointment import AppointmentCreate, AppointmentRead
from app.schemas.doctor import DoctorCreate, DoctorRead
from app.schemas.patient import PatientCreate, PatientRead
from app.services import appointment_service, doctor_service, patient_service

app = FastAPI(
    title="Hospital Appointment Management API",
    version="1.0.0",
)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/patients", response_model=list[PatientRead])
def list_patients(db: Session = Depends(get_db)):
    return patient_service.list_patients(db)


@app.post("/patients", response_model=PatientRead, status_code=201)
def create_patient(data: PatientCreate, db: Session = Depends(get_db)):
    return patient_service.create_patient(db, data)


@app.get("/patients/{patient_id}", response_model=PatientRead)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = patient_service.get_patient(db, patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@app.get("/doctors", response_model=list[DoctorRead])
def list_doctors(db: Session = Depends(get_db)):
    return doctor_service.list_doctors(db)


@app.post("/doctors", response_model=DoctorRead, status_code=201)
def create_doctor(data: DoctorCreate, db: Session = Depends(get_db)):
    return doctor_service.create_doctor(db, data)


@app.get("/doctors/{doctor_id}", response_model=DoctorRead)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = doctor_service.get_doctor(db, doctor_id)
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


@app.get("/appointments", response_model=list[AppointmentRead])
def list_appointments(db: Session = Depends(get_db)):
    return appointment_service.list_appointments(db)


@app.post("/appointments", response_model=AppointmentRead, status_code=201)
def create_appointment(data: AppointmentCreate, db: Session = Depends(get_db)):
    return appointment_service.create_appointment(db, data)


@app.get("/appointments/{appointment_id}", response_model=AppointmentRead)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = appointment_service.get_appointment(db, appointment_id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment
