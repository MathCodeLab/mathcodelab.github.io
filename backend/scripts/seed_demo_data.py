import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app import database, models, crud, schemas
from sqlalchemy.orm import Session
from datetime import datetime

def seed():
    db = next(database.get_db())
    # Valid certificate
    cert1 = schemas.CertificateCreate(
        student_name="Alice Example",
        course_title="Python Programming Basics",
        completion_date="2026-04-20",
        duration_hours=20
    )
    c1 = crud.create_certificate(db, cert1)
    # Another demo certificate
    cert2 = schemas.CertificateCreate(
        student_name="Bob Example",
        course_title="Data Science Intro",
        completion_date="2026-03-15",
        duration_hours=15
    )
    c2 = crud.create_certificate(db, cert2)
    print(f"Seeded: {c1.certificate_id}, {c2.certificate_id}")

if __name__ == "__main__":
    seed()
