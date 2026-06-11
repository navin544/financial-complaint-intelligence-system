from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from .database import Base
import datetime

class ComplaintRecord(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(String, index=True)
    text = Column(Text)
    category = Column(String)
    confidence = Column(Float)
    summary = Column(Text)
    sentiment = Column(String)
    urgency = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
