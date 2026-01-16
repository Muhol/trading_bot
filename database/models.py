from sqlalchemy import Column, Integer, Float, String, Boolean
from database.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    whatsapp_number = Column(String, unique=True, nullable=False)

    account_balance = Column(Float, nullable=False)
    risk_percent = Column(Float, default=1.0)

    min_lot = Column(Float, default=0.001)
    max_lot = Column(Float, default=1.0)

    receive_signals = Column(Boolean, default=True)
    receive_high_profit_only = Column(Boolean, default=False)
