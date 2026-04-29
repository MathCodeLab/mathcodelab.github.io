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
    attendance_percentage = int(input("Attendance percentage (0-100): "))
    assignment_completion_percentage = int(input("Assignment completion percentage (0-100): "))
    course_level = input("Course level (e.g. Master-level, Bachelor-level, High School-level): ")
    course_format = input("Course format (e.g. Online (via Zoom), In-person, Hybrid): ")
    instruction_language = input("Instruction language (e.g. English, German, Arabic): ") 
    cert_in = schemas.CertificateCreate(
        student_name=student_name,
        course_title=course_title,
        completion_date=completion_date,
        duration_hours=duration_hours,
        attendance_percentage=attendance_percentage,
        assignment_completion_percentage=assignment_completion_percentage,
        course_level=course_level,
        course_format=course_format,
        instruction_language=instruction_language
    )
    cert = crud.create_certificate(db, cert_in)
    print(f"Created certificate: {cert.certificate_id}")
    print(f"Verification URL: https://mathcodelab.de/verify/?id={cert.certificate_id}")

if __name__ == "__main__":
    main()
