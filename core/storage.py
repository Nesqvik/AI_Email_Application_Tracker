# app/tools/storage.py

from sqlalchemy import create_engine, Column, String, Boolean, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import DateTime
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "data", "db.sqlite")

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

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
        return

    email = Email(**data)
    db.add(email)
    db.commit()
    db.close()

def get_all_job_emails():
    db = SessionLocal()
    data = db.query(Email).filter_by(is_job_related=True).all()
    db.close()
    return data