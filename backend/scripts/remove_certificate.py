import argparse
import os
import sys

from dotenv import load_dotenv
from sqlalchemy.orm import Session

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))
sys.path.append(PROJECT_ROOT)

from app import crud, database


def remove_certificates_by_student(student_id: str):
    database.ensure_certificate_schema()
    db: Session = next(database.get_db())
    try:
        deleted_count = crud.delete_certificates_by_student_id(db, student_id)
        if deleted_count == 0:
            print(f"No certificates found for student_id: {student_id}")
            return 1

        print(f"Deleted {deleted_count} certificate(s) for student_id: {student_id}")
        return 0
    except Exception as exc:
        print("Error while deleting certificates:")
        print(exc)
        return 1
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description="Delete certificates by student_id (bulk)")
    parser.add_argument("student_id", help="Student ID, e.g. S12345")
    args = parser.parse_args()

    raise SystemExit(remove_certificates_by_student(args.student_id.strip()))


if __name__ == "__main__":
    main()
