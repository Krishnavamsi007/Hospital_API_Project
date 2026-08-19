from pydantic import BaseModel, ConfigDict, Field


class DoctorCreate(BaseModel):
    name: str = Field(..., min_length=1)
    specialization: str = Field(..., min_length=1)


class DoctorRead(DoctorCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
