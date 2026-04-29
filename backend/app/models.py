from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Student(Base):
    __tablename__ = "students"
    student_id = Column(String, primary_key=True, index=True, nullable=False)
    student_name = Column(String, nullable=False)
    created_at = Column(Date, server_default=func.current_date())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

class Certificate(Base):
    __tablename__ = "certificates"
    id = Column(Integer, primary_key=True, index=True)
    certificate_id = Column(String, unique=True, index=True, nullable=False)
    student_id = Column(String, ForeignKey("students.student_id"), index=True, nullable=False)
    student_name = Column(String, nullable=False)
    course_title = Column(String, nullable=False)
    completion_date = Column(String, nullable=False)
    duration_hours = Column(Integer, nullable=False)
    attendance_percentage = Column(Integer, nullable=True)
    assignment_completion_percentage = Column(Integer, nullable=True)
    course_level = Column(String, nullable=True)
    course_format = Column(String, nullable=True)
    instruction_language = Column(String, nullable=True)
    course_link = Column(String, nullable=True)
    status = Column(String, default="valid", server_default="valid", nullable=False)
    
    issuer = Column(String, default="MathCodeLab", nullable=False)
    instructor = Column(String, default="Mohammad Orabe", nullable=False)
    student = relationship("Student")
    created_at = Column(Date, server_default=func.current_date())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
