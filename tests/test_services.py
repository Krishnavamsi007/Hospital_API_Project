from datetime import datetime, timedelta, timezone

import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models.models import Appointment, Doctor, Patient
from app.schemas.appointment import AppointmentCreate
from app.services.appointment_service import create_appointment


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=engine)
    SessionLocalTest = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    db = SessionLocalTest()
    try:
        yield db
    finally:
        db.close()
        engine.dispose()


def create_patient(db, name="Peter Parker", email="peter.parker@example.com"):
    patient = Patient(name=name, email=email, phone="9999999999")
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


def create_doctor(db, name="Tony Stark", specialization="General"):
    doctor = Doctor(name=name, specialization=specialization)
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


def test_service_creates_valid_appointment(db_session):
    patient = create_patient(db_session)
    doctor = create_doctor(db_session)
    start = datetime.now(timezone.utc) + timedelta(hours=1)
    end = start + timedelta(minutes=30)

    appointment = create_appointment(
        db_session,
        AppointmentCreate(
            patient_id=patient.id,
            doctor_id=doctor.id,
            appointment_start=start,
            appointment_end=end,
        ),
    )

    assert appointment.id is not None
    assert appointment.doctor_id == doctor.id


def test_service_rejects_overlapping_appointments(db_session):
    patient = create_patient(db_session)
    doctor = create_doctor(db_session)
    start = datetime.now(timezone.utc) + timedelta(hours=2)

    create_appointment(
        db_session,
        AppointmentCreate(
            patient_id=patient.id,
            doctor_id=doctor.id,
            appointment_start=start,
            appointment_end=start + timedelta(minutes=60),
        ),
    )

    with pytest.raises(HTTPException) as exc:
        create_appointment(
            db_session,
            AppointmentCreate(
                patient_id=patient.id,
                doctor_id=doctor.id,
                appointment_start=start + timedelta(minutes=30),
                appointment_end=start + timedelta(minutes=90),
            ),
        )

    assert exc.value.status_code == 409


def test_service_allows_back_to_back_appointments(db_session):
    patient = create_patient(db_session)
    doctor = create_doctor(db_session)
    start = datetime.now(timezone.utc) + timedelta(hours=3)

    first = create_appointment(
        db_session,
        AppointmentCreate(
            patient_id=patient.id,
            doctor_id=doctor.id,
            appointment_start=start,
            appointment_end=start + timedelta(minutes=30),
        ),
    )
    second = create_appointment(
        db_session,
        AppointmentCreate(
            patient_id=patient.id,
            doctor_id=doctor.id,
            appointment_start=start + timedelta(minutes=30),
            appointment_end=start + timedelta(minutes=60),
        ),
    )

    assert first.id is not None
    assert second.id is not None


def test_service_rejects_end_before_start(db_session):
    patient = create_patient(db_session)
    doctor = create_doctor(db_session)
    start = datetime.now(timezone.utc) + timedelta(hours=4)

    with pytest.raises(HTTPException):
        create_appointment(
            db_session,
            AppointmentCreate(
                patient_id=patient.id,
                doctor_id=doctor.id,
                appointment_start=start + timedelta(minutes=30),
                appointment_end=start,
            ),
        )


def test_service_returns_appointments(db_session):
    patient = create_patient(db_session)
    doctor = create_doctor(db_session)
    start = datetime.now(timezone.utc) + timedelta(hours=5)
    appointment = create_appointment(
        db_session,
        AppointmentCreate(
            patient_id=patient.id,
            doctor_id=doctor.id,
            appointment_start=start,
            appointment_end=start + timedelta(minutes=45),
        ),
    )

    assert db_session.get(Appointment, appointment.id) is not None
