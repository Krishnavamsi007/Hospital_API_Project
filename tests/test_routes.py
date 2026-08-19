from datetime import datetime, timedelta, timezone


def test_create_and_get_patient(client):
    res = client.post(
        "/patients",
        json={
            "name": "Peter Parker",
            "email": "peter.parker@example.com",
            "phone": "9876543210",
        },
    )
    assert res.status_code == 201
    patient_id = res.json()["id"]

    res = client.get(f"/patients/{patient_id}")
    assert res.status_code == 200
    assert res.json()["email"] == "peter.parker@example.com"


def test_create_patient_duplicate_email_conflict(client):
    payload = {
        "name": "Duplicate User",
        "email": "duplicate@test.com",
        "phone": "5555555555",
    }

    first = client.post("/patients", json=payload)
    assert first.status_code == 201

    second = client.post("/patients", json=payload)
    assert second.status_code == 409
    assert second.json()["detail"] == "Patient with this email already exists"


def test_get_patient_not_found(client):
    res = client.get("/patients/999")
    assert res.status_code == 404


def test_list_patients(client):
    client.post(
        "/patients",
        json={
            "name": "Mary Jane",
            "email": "mary.jane@example.com",
            "phone": "1111111111",
        },
    )
    res = client.get("/patients")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_create_and_get_doctor(client):
    res = client.post(
        "/doctors",
        json={
            "name": "Tony Stark",
            "specialization": "Cardiology",
        },
    )
    assert res.status_code == 201
    doctor_id = res.json()["id"]

    res = client.get(f"/doctors/{doctor_id}")
    assert res.status_code == 200
    assert res.json()["specialization"] == "Cardiology"


def test_list_doctors(client):
    client.post(
        "/doctors",
        json={
            "name": "Steve Rogers",
            "specialization": "Neurology",
        },
    )
    res = client.get("/doctors")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_create_appointment(client):
    patient = client.post(
        "/patients",
        json={
            "name": "Peter Parker",
            "email": "peter.parker@example.com",
            "phone": "9876543210",
        },
    ).json()

    doctor = client.post(
        "/doctors",
        json={
            "name": "Tony Stark",
            "specialization": "General",
        },
    ).json()

    start_time = datetime.now(timezone.utc) + timedelta(hours=1)
    end_time = start_time + timedelta(minutes=30)

    res = client.post(
        "/appointments",
        json={
            "patient_id": patient["id"],
            "doctor_id": doctor["id"],
            "appointment_start": start_time.isoformat(),
            "appointment_end": end_time.isoformat(),
        },
    )

    assert res.status_code == 201
    assert res.json()["doctor_id"] == doctor["id"]


def test_overlapping_appointments_conflict(client):
    patient = client.post(
        "/patients",
        json={
            "name": "Bruce Banner",
            "email": "bruce.banner@example.com",
            "phone": "2222222222",
        },
    ).json()

    doctor = client.post(
        "/doctors",
        json={
            "name": "Tony Stark",
            "specialization": "General",
        },
    ).json()

    start_time = datetime.now(timezone.utc) + timedelta(hours=2)
    res1 = client.post(
        "/appointments",
        json={
            "patient_id": patient["id"],
            "doctor_id": doctor["id"],
            "appointment_start": start_time.isoformat(),
            "appointment_end": (start_time + timedelta(minutes=60)).isoformat(),
        },
    )
    assert res1.status_code == 201

    res2 = client.post(
        "/appointments",
        json={
            "patient_id": patient["id"],
            "doctor_id": doctor["id"],
            "appointment_start": (start_time + timedelta(minutes=30)).isoformat(),
            "appointment_end": (start_time + timedelta(minutes=90)).isoformat(),
        },
    )

    assert res2.status_code == 409


def test_back_to_back_appointments_allowed(client):
    patient = client.post(
        "/patients",
        json={
            "name": "Natasha Romanoff",
            "email": "natasha.romanoff@example.com",
            "phone": "3333333333",
        },
    ).json()
    doctor = client.post(
        "/doctors",
        json={
            "name": "Tony Stark",
            "specialization": "General",
        },
    ).json()

    start_time = datetime.now(timezone.utc) + timedelta(hours=3)
    first = client.post(
        "/appointments",
        json={
            "patient_id": patient["id"],
            "doctor_id": doctor["id"],
            "appointment_start": start_time.isoformat(),
            "appointment_end": (start_time + timedelta(minutes=30)).isoformat(),
        },
    )
    assert first.status_code == 201

    second = client.post(
        "/appointments",
        json={
            "patient_id": patient["id"],
            "doctor_id": doctor["id"],
            "appointment_start": (start_time + timedelta(minutes=30)).isoformat(),
            "appointment_end": (start_time + timedelta(minutes=60)).isoformat(),
        },
    )
    assert second.status_code == 201


def test_get_appointment_not_found(client):
    res = client.get("/appointments/999")
    assert res.status_code == 404


def test_list_appointments(client):
    res = client.get("/appointments")
    assert res.status_code == 200
    assert isinstance(res.json(), list)
