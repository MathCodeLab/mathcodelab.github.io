from pydantic import BaseModel, Field
from typing import Optional

class CertificateBase(BaseModel):
    student_id: str
    student_name: str
    course_title: str
    completion_date: str
    duration_hours: int
    created_at: Optional[str] = None
    attendance_percentage: Optional[int] = None
    assignment_completion_percentage: Optional[int] = None
    course_level: Optional[str] = None
    course_format: Optional[str] = None
    instruction_language: Optional[str] = None
    course_link: Optional[str] = None
    issuer: Optional[str] = "MathCodeLab"
    instructor: Optional[str] = "Mohammad Orabe"

class CertificateCreate(CertificateBase):
    pass

class CertificateOut(CertificateBase):
    certificate_id: str
    class Config:
        from_attributes = True


class StudentOut(BaseModel):
    student_id: str
    student_name: str


class StudentLookupResponse(BaseModel):
    student: StudentOut
    certificates: list[CertificateOut]

class CertificateVerificationResponse(BaseModel):
    status: str
    certificate_id: str
    verification_url: Optional[str] = None
    student_id: Optional[str] = None
    student_name: Optional[str] = None
    course_title: Optional[str] = None
    course_link: Optional[str] = None
    completion_date: Optional[str] = None
    duration_hours: Optional[int] = None
    issuer: Optional[str] = None
    instructor: Optional[str] = None
    verified_at: Optional[str] = None
    message: Optional[str] = None
    attendance_percentage: Optional[int] = None
    assignment_completion_percentage: Optional[int] = None
    course_level: Optional[str] = None
    course_format: Optional[str] = None
    instruction_language: Optional[str] = None
    # Certificate creation date (date-only)
    certificate_created_at: Optional[str] = None


class CertificateDeleteResponse(BaseModel):
    message: str
    student_id: str
    deleted_count: int
    
# Revocation support removed: no revoke schema
