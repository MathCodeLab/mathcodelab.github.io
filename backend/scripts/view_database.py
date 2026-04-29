import os
import sys
from datetime import datetime, timezone

try:
	from dotenv import load_dotenv
except ModuleNotFoundError:
	load_dotenv = None

from sqlalchemy.orm import Session

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if load_dotenv:
	load_dotenv(os.path.join(PROJECT_ROOT, ".env"))
else:
	# fallback: load simple KEY=VALUE pairs into env if .env exists
	env_path = os.path.join(PROJECT_ROOT, ".env")
	if os.path.exists(env_path):
		with open(env_path, "r", encoding="utf-8") as f:
			for raw in f:
				line = raw.strip()
				if not line or line.startswith("#") or "=" not in line:
					continue
				k, v = line.split("=", 1)
				os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

sys.path.append(PROJECT_ROOT)

from app import database
from app.database import SessionLocal
from app.models import Certificate


def _format_dt(dt: datetime) -> str:
	if not dt:
		return "-"
	# ensure timezone-aware
	if dt.tzinfo is None:
		dt = dt.replace(tzinfo=timezone.utc)
	# convert to local timezone for display
	try:
		local = dt.astimezone()
	except Exception:
		local = dt
	return local.strftime("%d.%m.%Y, %H:%M %Z")


def view_database(limit: int = 50):
	# Ensure missing optional columns are added before selecting all model fields.
	database.ensure_certificate_schema()
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
			print(f"Student ID     : {cert.student_id}")
			print(f"Student Name   : {cert.student_name}")
			print(f"Course Title   : {cert.course_title}")
			print(f"Completion Date: {cert.completion_date}")
			print(f"Duration       : {cert.duration_hours} hours")
			print(f"Issuer         : {cert.issuer}")
			print(f"Instructor     : {cert.instructor}")
			print(f"Course Link    : {cert.course_link or '-'}")
			print(f"Status         : {getattr(cert, 'status', 'valid')}")
			print(f"Created At     : {_format_dt(cert.created_at)}")
			print("=" * 50)

	except Exception as e:
		print("Error while fetching data:")
		print(e)
	finally:
		db.close()


if __name__ == "__main__":
	view_database()
