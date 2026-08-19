from pydantic import BaseModel, ConfigDict, EmailStr, Field


class PatientCreate(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    phone: str


class PatientRead(PatientCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
