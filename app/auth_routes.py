from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import get_db
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from app.schemas import UserLogin
import jwt


# Parolni hashlash uchun CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")
# JWT uchun kalit va algoritm
SECRET_KEY = "4824f48f47d53de857a6c710e5cf77bd"  # O'zgartiring
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

# Access token yaratish funksiyasi
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})  # Token muddati
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Token kodlash
    return encoded_jwt




def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username


# Foydalanuvchini ro'yxatdan o'tkazish
@router.post("/api/register/", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)  # Foydalanuvchini tekshirish
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Parolni hashlash
    hashed_password = pwd_context.hash(user.password)

    # Yangi foydalanuvchini yaratish
    user_data = schemas.UserCreate(
        username=user.username,
        email=user.email,
        password=user.password  # bu yerda passwordni saqlamaymiz, faqat parolni hashlashni xohlaymiz
    )

    return crud.create_user(db=db, user=user_data)

# Foydalanuvchini kirish
@router.post("/api/login/")
def login(user: UserLogin, db: Session = Depends(get_db)):
    # Foydalanuvchini olish
    user_in_db = crud.get_user_by_username(db, user.username)
    if not user_in_db or not pwd_context.verify(user.password, user_in_db.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Access token yaratish
    access_token = create_access_token(data={"sub": user_in_db.username})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/api/profile/")
def read_users_me(current_user: str = Depends(get_current_user)):
    return {"username": current_user}
