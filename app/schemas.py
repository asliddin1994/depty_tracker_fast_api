from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Literal

class DebtType(str, Enum):
    owed_to = "Olingan"
    owed_by = "Berilgan"
    individual = "Individual"

class DebtBase(BaseModel):
    debt_type: DebtType
    person_name: str
    amount: float
    currency: str
    description: str
    due_date: datetime

class DebtCreate(BaseModel):
    debt_type: Literal["owed_to", "owed_by", "individual"]
    person_name: str
    amount: float
    currency: str  # UZS, USD va h.k.
    description: str
    due_date: datetime

class Debt(DebtBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class SettingsBase(BaseModel):
    key: str
    value: str

class SettingsCreate(SettingsBase):
    pass

class SettingsUpdate(SettingsBase):
    pass

class Settings(SettingsBase):
    id: int

    class Config:
        orm_mode = True
