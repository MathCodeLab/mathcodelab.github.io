import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app import database, models, crud, schemas
from sqlalchemy.orm import Session

def main():
    db = next(database.get_db())
    print("Enter certificate details:")
    student_name = input("Student name: ")
    course_title = input("Course title: ")
    completion_date = input("Completion date (YYYY-MM-DD): ")
    duration_hours = int(input("Duration (hours): "))
    cert_in = schemas.CertificateCreate(
        student_name=student_name,
        course_title=course_title,
        completion_date=completion_date,
        duration_hours=duration_hours
    )
    cert = crud.create_certificate(db, cert_in)
    print(f"Created certificate: {cert.certificate_id}")

if __name__ == "__main__":
    main()
