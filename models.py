from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class URLItem(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, index=True)
    short_key = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    clicks = Column(Integer, default=0)