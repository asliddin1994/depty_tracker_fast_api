from fastapi import FastAPI, Depends, HTTPException
from app.routes import router
from sqlalchemy.orm import Session
from .database import get_db
from .crud import get_settings, get_setting, update_setting, create_setting
from .schemas import Settings, SettingsUpdate, SettingsCreate
from app import auth_routes

app = FastAPI()

app.include_router(router)
app.include_router(auth_routes.router)


@app.get("/")
def read_root():
    return f"Hello, World!"


@app.get("/api/settings/", response_model=list[Settings])
def read_settings(db: Session = Depends(get_db)):
    return get_settings(db)

@app.post("/api/settings/", response_model=Settings)
def create_setting_endpoint(setting: SettingsCreate, db: Session = Depends(get_db)):
    return create_setting(
        db,
        key=setting.key,
        value=setting.value,
        reminder_time=setting.reminder_time,
        currency=setting.currency,
    )


@app.put("/api/settings/{setting_id}", response_model=Settings)
def update_setting_endpoint(setting_id: int, setting_update: SettingsUpdate, db: Session = Depends(get_db)):
    updated_setting = update_setting(db, setting_id, setting_update)
    if updated_setting is None:
        raise HTTPException(status_code=404, detail="Setting not found")
    return updated_setting