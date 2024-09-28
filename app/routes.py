from . import crud
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine, get_db
from datetime import datetime
from .crud import get_debt_statistics, get_settings, get_setting, update_setting, get_user_by_username

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/api/monitoring/")
def get_monitoring_statistics(db: Session = Depends(get_db)):
    stats = get_debt_statistics(db)
    return stats

@router.post("/api/debts/")
def create_debt(debt: schemas.DebtCreate, db: Session = Depends(get_db)):
    db_debt = models.Debt(**debt.dict(), created_at=datetime.now())
    db.add(db_debt)
    db.commit()
    db.refresh(db_debt)
    return db_debt

@router.put("/api/debts/{debt_id}")
def update_debt(debt_id: int, debt: schemas.DebtCreate, db: Session = Depends(get_db)):
    db_debt = db.query(models.Debt).filter(models.Debt.id == debt_id).first()
    if db_debt is None:
        return {"error": "Debt not found"}

    for key, value in debt.dict().items():
        setattr(db_debt, key, value)

    db.commit()
    db.refresh(db_debt)
    return db_debt

@router.delete("/api/debts/{debt_id}")
def delete_debt(debt_id: int, db: Session = Depends(get_db)):
    db_debt = db.query(models.Debt).filter(models.Debt.id == debt_id).first()
    if db_debt is None:
        return {"error": "Debt not found"}

    db.delete(db_debt)
    db.commit()
    return {"message": "Debt deleted successfully"}



@router.get("/api/debts/", response_model=list[schemas.Debt] )
def read_debts(debt_type: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Debt)

    if debt_type:
        if debt_type == "individual":
            query = query.filter(models.Debt.debt_type == DebtType.individual)
        else:
            query = query.filter(models.Debt.debt_type == debt_type)

    debts = query.all()
    return debts


@router.post("/api/register/", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@router.post("/api/login/")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username)
    if not user or not crud.pwd_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful", "user_id": user.id}
