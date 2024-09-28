from sqlalchemy.orm import Session
from .models import Settings, Debt, User
from .schemas import SettingsCreate, SettingsUpdate, UserCreate
from passlib.context import CryptContext
from sqlalchemy import func


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_settings(db: Session):
    return db.query(Settings).all()

def get_setting(db: Session, setting_id: int):
    return db.query(Settings).filter(Settings.id == setting_id).first()

def update_setting(db: Session, setting_id: int, setting_update: SettingsUpdate):
    setting = db.query(Settings).filter(Settings.id == setting_id).first()
    if setting:
        setting.key = setting_update.key
        setting.value = setting_update.value
        db.commit()
        db.refresh(setting)
        return setting
    return None

def get_debt_statistics(db: Session):
    total_debts = db.query(Debt).count()
    total_amount = db.query(func.sum(Debt.amount)).scalar() or 0
    return {
        "total_debts": total_debts,
        "total_amount": total_amount,
    }


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user