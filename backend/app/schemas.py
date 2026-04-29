from pydantic import BaseModel, Field
from typing import Optional

class CertificateBase(BaseModel):
    student_name: str
    course_title: str
    completion_date: str
    duration_hours: int
    issuer: Optional[str] = "MathCodeLab"
    instructor: Optional[str] = "Mohammad Orabe"

class CertificateCreate(CertificateBase):
    pass

class CertificateOut(CertificateBase):
    certificate_id: str
    status: str
    revocation_reason: Optional[str] = None
    class Config:
        from_attributes = True

class CertificateVerificationResponse(BaseModel):
    status: str
    certificate_id: str
    verification_url: Optional[str] = None
    student_name: Optional[str] = None
    course_title: Optional[str] = None
    completion_date: Optional[str] = None
    duration_hours: Optional[int] = None
    issuer: Optional[str] = None
    instructor: Optional[str] = None
    verified_at: Optional[str] = None
    revocation_reason: Optional[str] = None
    message: Optional[str] = None
    attendance_percentage: Optional[int] = None
    assignment_completion_percentage: Optional[int] = None
    course_level: Optional[str] = None
    course_format: Optional[str] = None
    instruction_language: Optional[str] = None
    
class CertificateRevoke(BaseModel):
    revocation_reason: Optional[str] = None
