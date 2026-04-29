from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime
import random, string

def generate_certificate_id(year: int) -> str:
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
    return f"MCL-{year}-{random_part}"

def get_certificate_by_public_id(db: Session, certificate_id: str):
    return db.query(models.Certificate).filter(models.Certificate.certificate_id == certificate_id).first()

def create_certificate(db: Session, cert_in: schemas.CertificateCreate):
    year = datetime.utcnow().year

    while True:
        cert_id = generate_certificate_id(year)
        if not get_certificate_by_public_id(db, cert_id):
            break

    cert = models.Certificate(
        certificate_id=cert_id,
        student_name=cert_in.student_name,
        course_title=cert_in.course_title,
        completion_date=cert_in.completion_date,
        duration_hours=cert_in.duration_hours,
        attendance_percentage=cert_in.attendance_percentage,
        assignment_completion_percentage=cert_in.assignment_completion_percentage,
        course_level=cert_in.course_level,
        course_format=cert_in.course_format,
        instruction_language=cert_in.instruction_language,
        issuer=cert_in.issuer or "MathCodeLab",
        instructor=cert_in.instructor or "Mohammad Orabe",
    )

    db.add(cert)
    db.commit()
    db.refresh(cert)
    return cert

def revoke_certificate(db: Session, certificate_id: str, reason: str = None):
    cert = get_certificate_by_public_id(db, certificate_id)
    if not cert:
        return None
    # Revocation removed: function retained only for compatibility but does nothing
    return None
