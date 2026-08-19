from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AppointmentCreate(BaseModel):
    patient_id: int = Field(..., gt=0)
    doctor_id: int = Field(..., gt=0)
    appointment_start: datetime
    appointment_end: datetime


class AppointmentRead(AppointmentCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
