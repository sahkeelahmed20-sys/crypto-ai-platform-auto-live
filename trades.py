from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database import Base

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True)
    user = Column(String)
    pair = Column(String)
    side = Column(String)
    entry = Column(Float)
    exit = Column(Float)
    profit = Column(Float)
    time = Column(DateTime, default=datetime.utcnow)
