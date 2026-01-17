from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

class Complaint(Base):
    __tablename__ = "complaints"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    location = Column(String)
    complaint_type = Column(String)
    status = Column(String, default="Pending")

class PollutionData(Base):
    __tablename__ = "pollution_data"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, nullable=False)
    pm25 = Column(Float, nullable=False)
    pm10 = Column(Float, nullable=False)
    no2 = Column(Float, nullable=True)
    aqi = Column(Integer)

    recorded_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.id"))
