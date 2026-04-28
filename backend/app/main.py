import os
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from datetime import datetime
from . import models, schemas, crud, database, security

app = FastAPI(title="MathCodeLab Certificate Verification API")

# CORS
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in ALLOWED_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
get_db = database.get_db

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/verify/{certificate_id}", response_model=schemas.CertificateVerificationResponse)
def verify_certificate(certificate_id: str, db: Session = Depends(get_db)):
    cert = crud.get_certificate_by_public_id(db, certificate_id)
    if not cert:
        return JSONResponse(status_code=404, content={
            "status": "invalid",
            "certificate_id": certificate_id,
            "message": "Certificate not found"
        })
    if cert.status == "revoked":
        return {
            "status": "revoked",
            "certificate_id": cert.certificate_id,
            "revocation_reason": cert.revocation_reason or ""
        }
    return {
        "status": "valid",
        "certificate_id": cert.certificate_id,
        "student_name": cert.student_name,
        "course_title": cert.course_title,
        "completion_date": cert.completion_date,
        "duration_hours": cert.duration_hours,
        "issuer": cert.issuer,
        "instructor": cert.instructor,
        "verified_at": datetime.utcnow().isoformat() + "Z"
    }

@app.post("/admin/certificates", response_model=schemas.CertificateOut)
def create_certificate(
    cert_in: schemas.CertificateCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(security.verify_api_key)
):
    return crud.create_certificate(db, cert_in)

@app.patch("/admin/certificates/{certificate_id}/revoke", response_model=schemas.CertificateOut)
def revoke_certificate(
    certificate_id: str,
    body: schemas.CertificateRevoke,
    db: Session = Depends(get_db),
    api_key: str = Depends(security.verify_api_key)
):
    cert = crud.revoke_certificate(db, certificate_id, body.revocation_reason)
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
    return cert
