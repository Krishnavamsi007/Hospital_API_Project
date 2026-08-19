from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import Doctor


def list_doctors(db: Session):
    return db.scalars(select(Doctor)).all()


def create_doctor(db: Session, data):
    doctor = Doctor(**data.model_dump())
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


def get_doctor(db: Session, doctor_id: int):
    return db.get(Doctor, doctor_id)
