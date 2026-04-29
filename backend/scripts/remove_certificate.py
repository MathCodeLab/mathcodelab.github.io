import argparse
import os
import sys

from dotenv import load_dotenv
from sqlalchemy.orm import Session

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))
sys.path.append(PROJECT_ROOT)

from app import crud, database


def remove_certificates_by_student(student_id: str, confirm: bool = False):
    database.ensure_certificate_schema()
    db: Session = next(database.get_db())
    try:
        # Preview
        certs = db.query(database.Base.metadata.tables['certificates']).filter_by(student_id=student_id).all() if False else None
        # Use ORM helper to get count
        deleted_count = crud.delete_certificates_by_student_id(db, student_id) if confirm else None

        if not confirm:
            # dry-run: show what would be deleted
            certs = db.query(crud.models.Certificate).filter(crud.models.Certificate.student_id == student_id).all()
            if not certs:
                print(f"No certificates found for student_id: {student_id}")
                return 1
            print(f"Certificates that would be deleted for student_id={student_id}:")
            for c in certs:
                print(f" - {c.certificate_id} (created_at={getattr(c, 'created_at', None)})")
            print("Run with --yes to actually delete these certificates.")
            return 0

        # perform deletion
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


def remove_certificate_by_certificate_id(certificate_id: str, confirm: bool = False):
    database.ensure_certificate_schema()
    db: Session = next(database.get_db())
    try:
        cert = crud.get_certificate_by_public_id(db, certificate_id)
        if not cert:
            print(f"No certificate found with id: {certificate_id}")
            return 1

        if not confirm:
            print("Certificate that would be deleted:")
            print(f" - {cert.certificate_id} (student_id={cert.student_id}, student_name={cert.student_name}, created_at={getattr(cert, 'created_at', None)})")
            print("Run with --yes to actually delete this certificate.")
            return 0

        deleted = crud.delete_certificate(db, certificate_id)
        if not deleted:
            print("Deletion failed or certificate not found during deletion")
            return 1
        print(f"Deleted certificate {certificate_id}")
        return 0
    except Exception as exc:
        print("Error while deleting certificate:")
        print(exc)
        return 1
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description="Delete certificates by student_id (bulk) or by certificate_id")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--student", "-s", help="Student ID, e.g. S12345")
    group.add_argument("--certificate", "-c", help="Certificate public ID, e.g. MCL-2026-XXXX")
    parser.add_argument("--yes", "-y", action="store_true", help="Perform deletions without prompting")
    args = parser.parse_args()

    if args.student:
        raise SystemExit(remove_certificates_by_student(args.student.strip(), confirm=args.yes))
    if args.certificate:
        raise SystemExit(remove_certificate_by_certificate_id(args.certificate.strip(), confirm=args.yes))


if __name__ == "__main__":
    main()
