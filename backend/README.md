# MathCodeLab Certificate Verification System

A professional, scalable certificate verification system for MathCodeLab, using FastAPI and SQLite, with a static frontend for public verification.

## Architecture
- **Frontend:** Static HTML/CSS/JS (GitHub Pages)
- **Backend:** FastAPI (Python), SQLite (SQLAlchemy)
- **API URL:** https://api.mathcodelab.de

## File Structure
```
verify/
  index.html
  verify.js
assets/
  css/
    style.css
backend/
  app/
    main.py
    database.py
    models.py
    schemas.py
    crud.py
    security.py
  scripts/
    create_certificate.py
    remove_certificate.py
    seed_demo_data.py
  requirements.txt
  README.md
.env.example
```

## Local Setup
1. **Clone the repo and enter backend:**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env as needed
   ```
2. **Initialize the database:**
   ```bash
   python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
   ```
3. **Seed demo data:**
   ```bash
   python scripts/seed_demo_data.py
   ```
4. **Run the server:**
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints
- `GET /health` — API health check
- `GET /verify/{certificate_id}` — Verify a certificate
- `POST /admin/certificates` — Create a certificate (admin, API key required)
- `GET /admin/students/{student_id}` — Look up a student and their certificates (admin, API key required)
- `DELETE /admin/certificates/student/{student_id}` — Delete all certificates for a student (admin, API key required)

## Issuing a Certificate
- Use the admin API or run `python scripts/create_certificate.py` interactively.
- The script now asks for a `student_id` primary key and the student name.
- After creation, it also generates a QR image in `backend/assets/qrcodes/` using the public verification URL.

## Removing a Certificate
- Preview deletion by student ID:
  ```bash
  ./venv/bin/python scripts/remove_certificate.py --student S12345
  ```
- Preview deletion by certificate ID:
  ```bash
  ./venv/bin/python scripts/remove_certificate.py --certificate MCL-2026-XXXXXXX
  ```
- Execute deletion with confirmation:
  ```bash
  ./venv/bin/python scripts/remove_certificate.py --student S12345 --yes
  ./venv/bin/python scripts/remove_certificate.py --certificate MCL-2026-XXXXXXX --yes
  ```
- The script removes certificates only. It does not delete the student row.

## Cleaning Broken Student IDs
- Use this when rows contain `NULL`, empty, or literal `None` in `student_id`.
- Dry-run:
  ```bash
  ./venv/bin/python scripts/clean_none_students.py
  ```
- Execute cleanup:
  ```bash
  ./venv/bin/python scripts/clean_none_students.py --yes
  ```
- This script deletes matching certificates and matching student rows.

## Looking Up a Student
- Run `python scripts/view_student.py --student S12345`
- Or call the admin API: `GET /admin/students/{student_id}`

## Viewing Database Data
- Show the latest certificates:
  ```bash
  ./venv/bin/python scripts/view_database.py
  ```
- Show a specific student and all of their certificates:
  ```bash
  ./venv/bin/python scripts/view_student.py --student S12345
  ```
- Both viewers print dates without time, using `YYYY.MM.DD`.

## Revocation
Revocation support has been removed from this codebase. Certificates cannot be revoked via the API.

## Frontend Integration
- The verification page (`verify/index.html`) calls the backend API at `https://api.mathcodelab.de/verify/{certificate_id}`.
- Supports both `/verify/?id=...` and `/verify/ID` URL formats.

## Environment Variables
- `DATABASE_URL` — e.g. `sqlite:///./certificates.db`
- `ADMIN_API_KEY` — API key for admin endpoints
- `ALLOWED_ORIGINS` — e.g. `https://mathcodelab.de,https://www.mathcodelab.de`

## Deployment
- Deploy backend to Railway, Render, Fly.io, etc.
- Use the production command:
  ```bash
  uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```
- Point `api.mathcodelab.de` to your backend host (CNAME or A record).
- Set CORS origins via `ALLOWED_ORIGINS`.

## Certificate PDF Integration
- Each certificate should display:
  - Student ID
  - Certificate ID (e.g. MCL-2026-XXXXXX)
  - Verification URL: `https://mathcodelab.de/verify/?id={certificate_id}`
  - (Optional) QR code to the same URL
- The verification page confirms MathCodeLab as the issuer, not external accreditation.

## QR Images
- QR images are generated server-side as transparent PNG files.
- Default output path: `backend/assets/qrcodes/{student_id}_{certificate_id}.png`
- The QR payload is the public verification URL only.

## Wording Policy
- Use “Certificate of Completion” or “Certificate of Participation”.
- Do **not** use “accredited”, “state-recognized”, “official degree”, or “diploma”.

---

For questions, contact Mohammad Orabe.
