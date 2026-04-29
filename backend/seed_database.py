from app.models import Base, Certificate
from app.database import engine, SessionLocal
from app.crud import create_certificate
from app.schemas import CertificateCreate

# Create the database schema
Base.metadata.create_all(bind=engine)

def seed_database():
    db = SessionLocal()
    try:
        certificates = [
            CertificateCreate(
                student_name="John Doe",
                course_title="Python Programming",
                completion_date="2026-04-01",
                duration_hours=40,
                issuer="MathCodeLab",
                instructor="Mohammad Orabe"
            ),
            CertificateCreate(
                student_name="Jane Smith",
                course_title="Data Science Basics",
                completion_date="2026-03-15",
                duration_hours=30,
                issuer="MathCodeLab",
                instructor="Mohammad Orabe"
            ),
            CertificateCreate(
                student_name="Alice Johnson",
                course_title="Advanced Java",
                completion_date="2026-02-20",
                duration_hours=50,
                issuer="MathCodeLab",
                instructor="Mohammad Orabe"
            )
        ]

        for cert in certificates:
            create_certificate(db, cert)

        print("Database seeded successfully!")
    except Exception as e:
        print(f"An error occurred while seeding the database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()