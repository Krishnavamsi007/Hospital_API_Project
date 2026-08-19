# Hospital Appointment Management API

A FastAPI-based API for managing patients, doctors, and appointments in a small hospital workflow.

## Features

- Patient registration and lookup
- Doctor registration and lookup
- Appointment creation and retrieval
- Appointment overlap validation for the same doctor
- SQLite database persistence
- OpenAPI/Swagger documentation

## Tech Stack

- Python 3.10+
- FastAPI
- SQLAlchemy
- SQLite
- Uvicorn
- Pytest
- Ruff
- Bandit

## Project Structure

```text
.
├── main.py
├── requirements.txt
├── pyproject.toml
├── alembic/
├── src/
│   ├── database.py
│   ├── main.py
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── __init__.py
├── tests/
├── hospital.db
└── README.md
```

## Setup

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3. Apply the database schema:

```powershell
.\.venv\Scripts\alembic.exe upgrade head
```

## Run the API

From the project root:

```powershell
uvicorn main:app --reload
```

The API will be available at:

- http://127.0.0.1:8000
- Swagger docs: http://127.0.0.1:8000/docs

## API Endpoints

### Patients

- `GET /patients`
- `POST /patients`
- `GET /patients/{patient_id}`

### Doctors

- `GET /doctors`
- `POST /doctors`
- `GET /doctors/{doctor_id}`

### Appointments

- `GET /appointments`
- `POST /appointments`
- `GET /appointments/{appointment_id}`

## Example Patient Payload

```json
{
  "name": "Peter Parker",
  "email": "peter.parker@example.com",
  "phone": "9876543210"
}
```

## Example Doctor Payload

```json
{
  "name": "Tony Stark",
  "specialization": "Cardiology"
}
```

## Example Appointment Payload

```json
{
  "patient_id": 1,
  "doctor_id": 1,
  "appointment_start": "2026-08-13T10:00:00+00:00",
  "appointment_end": "2026-08-13T10:30:00+00:00"
}
```

## Testing

Run the test suite:

```powershell
pytest
```

Run lint checks:

```powershell
ruff check .
```

## Notes

- The project uses SQLite for local development.
- The database file is created as `hospital.db` in the root directory.
- Duplicate patient emails are rejected with a `409 Conflict` response.
