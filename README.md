# WhatBytes - Healthcare Backend Assignment

A Django REST Framework backend for user authentication, patient records, doctor records, and patient-doctor assignments.

## Features

- User registration with name, email, and password.
- Login using email/password and JWT access/refresh tokens.
- Patient create, list, retrieve, update, and delete APIs.
- Doctor create, list, retrieve, update, and delete APIs.
- Patient-doctor assignment and removal APIs.
- Patients are private to the user who created them.
- A user can only create doctor assignments for their own patients.
- Input validation, useful error responses, and duplicate-assignment protection.
- PostgreSQL configuration through `DATABASE_URL`.
- SQLite fallback for a quick first run when PostgreSQL is not configured.

## Project structure

```text
whatbytes_healthcare_backend/
├── api/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── healthcare/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── .env.example
├── docker-compose.yml
├── manage.py
└── requirements.txt
```

## 1. Setup on Windows PowerShell

Open PowerShell in this project folder and run:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py runserver
```

If Python 3.12 is not installed, use `py -m venv .venv`.

The default local setup uses SQLite so the project can be started without installing PostgreSQL. To use PostgreSQL as required by the assignment, follow the next section.

## 2. Run with PostgreSQL

Docker Desktop must be installed and running. From the project folder:

```powershell
docker compose up -d
Copy-Item .env.example .env
```

Open `.env` and set:

```env
SECRET_KEY=use-a-long-random-secret-value
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5432/whatbytes_healthcare
```

Then run:

```powershell
python manage.py migrate
python manage.py runserver
```

When `DATABASE_URL` is set, Django uses PostgreSQL. Do not commit `.env` to GitHub.

## 3. API base URL

`http://127.0.0.1:8000/api/`

All endpoints except register and login require this header after login:

```text
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## 4. APIs

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/auth/register/` | Register user |
| POST | `/api/auth/login/` | Login and receive JWT |
| POST | `/api/patients/` | Add patient |
| GET | `/api/patients/` | List your patients |
| GET | `/api/patients/<id>/` | Get your patient |
| PUT/PATCH | `/api/patients/<id>/` | Update your patient |
| DELETE | `/api/patients/<id>/` | Delete your patient |
| POST | `/api/doctors/` | Add doctor |
| GET | `/api/doctors/` | List all doctors |
| GET | `/api/doctors/<id>/` | Get doctor |
| PUT/PATCH | `/api/doctors/<id>/` | Update doctor |
| DELETE | `/api/doctors/<id>/` | Delete doctor |
| POST | `/api/mappings/` | Assign doctor to patient |
| GET | `/api/mappings/` | List your patient-doctor mappings |
| GET | `/api/mappings/<patient_id>/` | See note below |
| DELETE | `/api/mappings/<mapping_id>/` | Remove assignment |

### Patient-specific doctor list

`GET /api/mappings/<patient_id>/` returns all doctor assignments for that patient, as requested. The `DELETE /api/mappings/<mapping_id>/` route removes one assignment. The response is limited to the logged-in user's own patients.

### Example request bodies

Register:

```json
{
  "name": "Demo User",
  "email": "demo@example.com",
  "password": "StrongPass123!"
}
```

Login:

```json
{
  "email": "demo@example.com",
  "password": "StrongPass123!"
}
```

Create patient:

```json
{
  "name": "Rahul Sharma",
  "age": 28,
  "gender": "Male",
  "address": "Nagpur",
  "phone": "9876543210"
}
```

Create doctor:

```json
{
  "name": "Dr. Meera Patil",
  "specialization": "Cardiology",
  "email": "meera@example.com",
  "phone": "9876543211",
  "address": "Nagpur"
}
```

Assign doctor:

```json
{
  "patient": 1,
  "doctor": 1
}
```

## 5. Test with Postman

1. Start the server.
2. Send the register request.
3. Send login and copy the `access` token.
4. For all patient, doctor, and mapping requests, add `Authorization: Bearer <access-token>`.
5. Create a patient and a doctor.
6. Assign the doctor using their numeric IDs.
7. Test list, detail, update, and delete operations.

## 6. Useful commands

```powershell
python manage.py check
python manage.py test
python manage.py createsuperuser
```

Admin page: `http://127.0.0.1:8000/admin/`

## Notes

- The `.env` file is local configuration and is excluded from Git.
- Patient records are visible only to their owner.
- Doctor records are shared across authenticated users, matching the assignment's “retrieve all doctors” requirement.
- Mapping records are visible only when they belong to the logged-in user's patients.
- This is an internship assignment demo, not a production-ready system for storing real patient medical data. Do not upload real patient information.
