from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from .database import Base
import enum

class CertificateStatus(str, enum.Enum):
    valid = "valid"
    revoked = "revoked"

class Certificate(Base):
    __tablename__ = "certificates"
    id = Column(Integer, primary_key=True, index=True)
    certificate_id = Column(String, unique=True, index=True, nullable=False)
    student_name = Column(String, nullable=False)
    course_title = Column(String, nullable=False)
    completion_date = Column(String, nullable=False)
    duration_hours = Column(Integer, nullable=False)
    issuer = Column(String, default="MathCodeLab", nullable=False)
    instructor = Column(String, default="Mohammad Orabe", nullable=False)
    status = Column(Enum(CertificateStatus), default=CertificateStatus.valid, nullable=False)
    revocation_reason = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
