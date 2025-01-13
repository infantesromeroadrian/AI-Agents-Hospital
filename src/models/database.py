from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class Patient(Base):
    __tablename__ = 'patients'
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(String(50), unique=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    date_of_birth = Column(DateTime)
    medical_history = Column(JSON)
    cases = relationship("Case", back_populates="patient")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Case(Base):
    __tablename__ = 'cases'
    
    id = Column(Integer, primary_key=True)
    case_id = Column(String(50), unique=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    symptoms = Column(Text)
    triage_evaluation = Column(JSON)
    specialist_evaluation = Column(JSON)
    pharmacy_review = Column(JSON)
    nursing_care = Column(JSON)
    administrative_plan = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="cases") 