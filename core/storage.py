from pathlib import Path
from sqlalchemy import create_engine, Column, String, Boolean, Float
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "db.sqlite"

DB_PATH.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(f"sqlite:///{DB_PATH}")
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class Email(Base):
    __tablename__ = "emails"

    id = Column(String, primary_key=True)
    company = Column(String)
    category = Column(String)
    summary = Column(String)
    is_job_related = Column(Boolean)
    confidence = Column(Float)
    date = Column(String)
    language = Column(String)


Base.metadata.create_all(engine)


def save_email(data):
    db = SessionLocal()

    if db.query(Email).filter_by(id=data["id"]).first():
        db.close()
        return

    db.add(Email(**data))
    db.commit()
    db.close()


def get_all_job_emails():
    db = SessionLocal()
    emails = db.query(Email).filter_by(is_job_related=True).all()
    db.close()
    return emails