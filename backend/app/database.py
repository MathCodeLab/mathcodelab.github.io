import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def ensure_certificate_schema(bind=None):
    """Create the certificates table and add any missing columns.

    This keeps older PostgreSQL/SQLite databases compatible when the
    certificate model gains new optional fields.
    """
    target = bind or engine

    # Make sure the table exists first.
    Base.metadata.create_all(bind=target)

    inspector = inspect(target)
    if "certificates" not in inspector.get_table_names():
        return

    existing_columns = {column["name"] for column in inspector.get_columns("certificates")}
    missing_statements = []

    if "attendance_percentage" not in existing_columns:
        missing_statements.append("ALTER TABLE certificates ADD COLUMN attendance_percentage INTEGER")
    if "assignment_completion_percentage" not in existing_columns:
        missing_statements.append("ALTER TABLE certificates ADD COLUMN assignment_completion_percentage INTEGER")
    if "course_level" not in existing_columns:
        missing_statements.append("ALTER TABLE certificates ADD COLUMN course_level VARCHAR")
    if "course_format" not in existing_columns:
        missing_statements.append("ALTER TABLE certificates ADD COLUMN course_format VARCHAR")
    if "instruction_language" not in existing_columns:
        missing_statements.append("ALTER TABLE certificates ADD COLUMN instruction_language VARCHAR")

    if not missing_statements:
        return

    with target.begin() as connection:
        for statement in missing_statements:
            connection.exec_driver_sql(statement)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()