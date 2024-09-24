from sqlalchemy.orm import Session
from .models import Settings, Debt
from .schemas import SettingsCreate, SettingsUpdate
from sqlalchemy import func

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
