from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
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

class TransactionRecord(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True, index=True)
    sender_id = Column(String, index=True)
    receiver_id = Column(String, index=True)
    amount = Column(Float)
    risk_level = Column(String)
    fraud_probability = Column(Float)
    is_fraud = Column(Boolean)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    risk_factors = Column(Text) # JSON string of top contributing factors
