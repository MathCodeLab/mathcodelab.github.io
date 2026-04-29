import argparse
import os
import sys
from datetime import datetime, date

from sqlalchemy.orm import Session

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))


def load_env_file(env_path: str):
    try:
        from dotenv import load_dotenv
    except ModuleNotFoundError:
        load_dotenv = None

    if load_dotenv is not None:
        load_dotenv(env_path)
        return

    if not os.path.exists(env_path):
        return

    with open(env_path, "r", encoding="utf-8") as env_file:
        for raw_line in env_file:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)


load_env_file(os.path.join(PROJECT_ROOT, ".env"))
sys.path.append(PROJECT_ROOT)


def _format_value(value):
    if value is None:
        return value
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return value


def view_student(student_id: str):
    from app import crud, database, models

    database.ensure_certificate_schema()
    db: Session = next(database.get_db())
    try:
        student = crud.get_student_by_id(db, student_id)
        if not student:
            print(f"Student not found: {student_id}")
            return 1

        certificates = (
            db.query(models.Certificate)
            .filter(models.Certificate.student_id == student_id)
            .order_by(models.Certificate.created_at.desc())
            .all()
        )

        print("=" * 80)
        print("STUDENT INFORMATION")
        print("=" * 80)
        print(f"Student ID:   {student.student_id}")
        print(f"Student Name: {student.student_name}")
        print()
        print(f"Total Certificates: {len(certificates)}")
        
        if not certificates:
            print("\nNo certificates found for this student.")
            return 0
        
        print()
        for i, cert in enumerate(certificates, 1):
            print("-" * 80)
            print(f"Certificate #{i}")
            print("-" * 80)
            print(f"  Certificate ID:    {cert.certificate_id}")
            print(f"  Course Title:      {cert.course_title}")
            print(f"  Course Link:       {cert.course_link or '-'}")
            print(f"  Completion Date:   {cert.completion_date}")
            print(f"  Certificate Date:  {_format_value(cert.created_at)}")
            print(f"  Duration (hours):  {cert.duration_hours}")
            print(f"  Attendance %:      {cert.attendance_percentage}%")
            print(f"  Assignment Comp %: {cert.assignment_completion_percentage}%")
            print(f"  Course Level:      {cert.course_level or '-'}")
            print(f"  Course Format:     {cert.course_format or '-'}")
            print(f"  Language:          {cert.instruction_language or '-'}")
            print(f"  Issuer:            {cert.issuer}")
            print(f"  Instructor:        {cert.instructor}")
            print(f"  Status:            {getattr(cert, 'status', 'valid')}")
            print()
        
        print("=" * 80)
        return 0
    except Exception as exc:
        print("Error while looking up student:")
        print(exc)
        return 1
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description="View student data by student_id")
    parser.add_argument("student_id", help="Student ID, e.g. S12345")
    args = parser.parse_args()

    raise SystemExit(view_student(args.student_id.strip()))


if __name__ == "__main__":
    main()
