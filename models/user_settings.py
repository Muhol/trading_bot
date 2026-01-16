from sqlalchemy import Column, Integer, Float, Boolean, ForeignKey, DateTime
from db.base import Base
from datetime import datetime

class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    account_balance = Column(Float, nullable=False)
    risk_percent = Column(Float, nullable=False)
    max_lot_size = Column(Float, nullable=True)
    confidence_threshold = Column(Float, default=70.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
