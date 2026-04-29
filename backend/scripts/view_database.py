import os
import sys

from dotenv import load_dotenv
from sqlalchemy.orm import Session

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.database import SessionLocal
from app.models import Certificate


load_dotenv()


def view_database(limit: int = 50):
	db: Session = SessionLocal()
	try:
		certificates = (
			db.query(Certificate)
			.order_by(Certificate.created_at.desc())
			.limit(limit)
			.all()
		)

		if not certificates:
			print("No certificates found in the database.")
			return

		print(f"\nShowing up to {limit} certificates:\n")

		for cert in certificates:
			print("=" * 50)
			print(f"Certificate ID : {cert.certificate_id}")
			print(f"Student Name   : {cert.student_name}")
			print(f"Course Title   : {cert.course_title}")
			print(f"Completion Date: {cert.completion_date}")
			print(f"Duration       : {cert.duration_hours} hours")
			print(f"Issuer         : {cert.issuer}")
			print(f"Instructor     : {cert.instructor}")
			print(f"Course Link    : {cert.course_link or '-'}")
			print(f"Status         : {getattr(cert, 'status', 'valid')}")
			print(f"Created At     : {cert.created_at}")
			print("=" * 50)

	except Exception as e:
		print("Error while fetching data:")
		print(e)
	finally:
		db.close()


if __name__ == "__main__":
	view_database()
