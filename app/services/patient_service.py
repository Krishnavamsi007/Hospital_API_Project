from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.models import Patient


def list_patients(db: Session):
    return db.scalars(select(Patient)).all()


def create_patient(db: Session, data):
    patient = Patient(**data.model_dump())
    db.add(patient)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Patient with this email already exists") from None
    db.refresh(patient)
    return patient


def get_patient(db: Session, patient_id: int):
    return db.get(Patient, patient_id)
