from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import Appointment, Doctor, Patient
from app.services.utils import ensure_utc


def list_appointments(db: Session):
    return db.scalars(select(Appointment)).all()


def get_appointment(db: Session, appointment_id: int):
    return db.get(Appointment, appointment_id)


def create_appointment(db: Session, data):
    patient = db.get(Patient, data.patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    doctor = db.get(Doctor, data.doctor_id)
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")

    appointment_start = ensure_utc(data.appointment_start)
    appointment_end = ensure_utc(data.appointment_end)

    if appointment_start >= appointment_end:
        raise HTTPException(
            status_code=400,
            detail="appointment_end must be after appointment_start",
        )

    existing_appointments = db.execute(
        select(Appointment).where(Appointment.doctor_id == data.doctor_id)
    ).scalars().all()

    for existing in existing_appointments:
        existing_start = ensure_utc(existing.appointment_start)
        existing_end = ensure_utc(existing.appointment_end)
        if existing_start < appointment_end and existing_end > appointment_start:
            raise HTTPException(
                status_code=409,
                detail="Appointment overlaps an existing appointment for this doctor.",
            )

    payload = data.model_dump()
    payload["appointment_start"] = appointment_start
    payload["appointment_end"] = appointment_end

    appointment = Appointment(**payload)
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment
