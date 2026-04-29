import sys
import os
from datetime import datetime
from dotenv import load_dotenv

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))
sys.path.append(PROJECT_ROOT)

from app import database, models, crud, schemas, qr
from sqlalchemy.orm import Session


def prompt_int(prompt, min_value=None, max_value=None):
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("Please enter a whole number.")
            continue

        if min_value is not None and value < min_value:
            print(f"Please enter a value of at least {min_value}.")
            continue
        if max_value is not None and value > max_value:
            print(f"Please enter a value of at most {max_value}.")
            continue

        return value


def prompt_date(prompt):
    while True:
        raw = input(prompt).strip()
        try:
            datetime.strptime(raw, "%Y-%m-%d")
            return raw
        except ValueError:
            print("Please enter a valid date in YYYY-MM-DD format.")


def prompt_optional_date(prompt):
    while True:
        raw = input(prompt).strip()
        if not raw:
            return None

        try:
            datetime.strptime(raw, "%Y-%m-%d")
            return raw
        except ValueError:
            print("Please enter a valid date in YYYY-MM-DD format, or leave blank.")

def main():
    database.ensure_certificate_schema()
    db = next(database.get_db())
    print("Enter certificate details:")
    
    student_id = input("1. Student ID (primary key, e.g. STU-2026-001): ").strip()
    student_name = input("2. Student name: ")
    course_title = input("3. Course title: ")
    completion_date = prompt_date("4. Completion date (YYYY-MM-DD): ")
    created_at = prompt_optional_date("5. Certificate creation date (YYYY-MM-DD, optional): ")
    duration_hours = prompt_int("6. Duration (hours): ", min_value=0)
    attendance_percentage = prompt_int("7. Attendance percentage (0-100): ", min_value=0, max_value=100)
    assignment_completion_percentage = prompt_int("8. Assignment completion percentage (0-100): ", min_value=0, max_value=100)
    course_level = input("9. Course level (e.g. Master-level, Bachelor-level, High School-level): ")
    course_format = input("10. Course format (e.g. Online (via Zoom), In-person, Hybrid): ")
    instruction_language = input("11. Instruction language (e.g. English, German, Arabic): ") 
    course_link = input("12. Course link (optional, e.g. https://...): ").strip() or None
    
    print("-" * 60)
    
    cert_in = schemas.CertificateCreate(
        student_id=student_id,
        student_name=student_name,
        course_title=course_title,
        completion_date=completion_date,
        duration_hours=duration_hours,
        created_at=created_at,
        attendance_percentage=attendance_percentage,
        assignment_completion_percentage=assignment_completion_percentage,
        course_level=course_level,
        course_format=course_format,
        instruction_language=instruction_language,
        course_link=course_link
    )
    cert = crud.create_certificate(db, cert_in)
    verification_url = qr.build_verification_url(cert.certificate_id)
    qr_path = qr.generate_certificate_qr(
        cert.certificate_id,
        student_id=cert.student_id,
        verification_url=verification_url,
    )
    print(f"Created certificate: {cert.certificate_id}")
    print(f"Verification URL: {verification_url}")
    print(f"QR image saved to: {qr_path}")

if __name__ == "__main__":
    main()
