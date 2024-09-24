from sqlalchemy import Column, Integer, String, Enum, DateTime, Float
from sqlalchemy.orm import relationship
from .database import Base
from enum import Enum as PyEnum
from datetime import datetime
from sqlalchemy.dialects.postgresql import ENUM

class DebtType(str, PyEnum):
    owed_to = "Olingan"
    owed_by = "Berilgan"

class Debt(Base):
    __tablename__ = "debts"

    id = Column(Integer, primary_key=True, index=True)
    debt_type = Column(ENUM(DebtType), nullable=False)
    person_name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    due_date = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<Debt {self.id}: {self.person_name}, {self.amount} {self.currency}>"



class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    value = Column(String)

    def __repr__(self):
        return f"<Settings(id={self.id}, key={self.key}, value={self.value})>"