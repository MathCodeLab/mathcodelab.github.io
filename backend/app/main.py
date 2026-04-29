import os
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from datetime import datetime
from . import models, schemas, crud, database, security
import os

ENABLE_DOCS = os.getenv("ENABLE_DOCS", "false").lower() == "true"

# How to access docs when needed:
# ENABLE_DOCS=true uvicorn app.main:app --reload
# http://127.0.0.1:8000/docs
# Temporary in production (optional):
# ENABLE_DOCS=true
# Then:
# * Redeploy
# * Use /docs
# * Then set back to false

app = FastAPI(
    title="MathCodeLab Certificate Verification API",
    docs_url="/docs" if ENABLE_DOCS else None,
    redoc_url="/redoc" if ENABLE_DOCS else None,
    openapi_url="/openapi.json" if ENABLE_DOCS else None,
)

database.ensure_certificate_schema()

# CORS
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in ALLOWED_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "service": "MathCodeLab Certificate Verification API",
        "status": "running",
        "health": "/health",
        "verify": "/verify/{certificate_id}",
        "docs": "/docs"
    }
    
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

    return {
        "status": "valid",
        "certificate_id": cert.certificate_id,
        "student_name": cert.student_name,
        "course_title": cert.course_title,
        "completion_date": cert.completion_date,
        "duration_hours": cert.duration_hours,
        "issuer": cert.issuer,
        "instructor": cert.instructor,
        "verified_at": datetime.utcnow().isoformat() + "Z",
        "verification_url": f"https://mathcodelab.de/verify/?id={cert.certificate_id}"
    }

@app.post("/admin/certificates", response_model=schemas.CertificateOut)
def create_certificate(
    cert_in: schemas.CertificateCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(security.verify_api_key)
):
    return crud.create_certificate(db, cert_in)

# Revocation endpoint removed

@app.get("/admin/certificates")
def list_certificates(
    db: Session = Depends(get_db),
    api_key: str = Depends(security.verify_api_key)
):
    certs = db.query(models.Certificate).all()
    return certs