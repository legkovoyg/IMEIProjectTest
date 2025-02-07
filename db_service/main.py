import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models.models_db import User, TelegramWhitelist, Base  # SQLAlchemy модели
from database.database import SessionLocal, engine
from models.models import (
    TokenRequest,
    TokenResponse,
    UserCreate,
    TelegramWhitelistCreate, TgRequest, TgResponse
)

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/telegram-whitelist/check", response_model=TgResponse)
def verify_user_tg(request: TgRequest, db: Session = Depends(get_db)):
    # Проверяем, есть ли уже запись в белом списке с таким telegram_id
    existing_tg = db.query(TelegramWhitelist).filter(
        TelegramWhitelist.telegram_id == request.telegram_id
    ).first()
    if not existing_tg:
        raise HTTPException(status_code=401, detail="Invalid tg")
    return TgResponse(valid=True, username=existing_tg.username)

@app.post("/users/check", response_model=TokenResponse)
def verify_user_token(request: TokenRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.token == request.token).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return TokenResponse(valid=True, username=user.username)

# Эндпоинт для добавления нового пользователя (таблица users)
@app.post("/users/add", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.token == user.token)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this username or token already exists")
    new_user = User(username=user.username, token=user.token)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user, {"message": "User created successfully"}

# Эндпоинт для добавления записи в белый список Telegram-пользователей (таблица telegram_whitelist)
@app.post("/telegram-whitelist/add", response_model=TelegramWhitelistCreate)
def create_telegram_whitelist(entry: TelegramWhitelistCreate, db: Session = Depends(get_db)):
    existing_entry = db.query(TelegramWhitelist).filter(
        TelegramWhitelist.telegram_id == entry.telegram_id
    ).first()
    if existing_entry:
        raise HTTPException(status_code=400, detail="Telegram user is already in whitelist")
    new_entry = TelegramWhitelist(telegram_id=entry.telegram_id, username=entry.username)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry, {"message": "TgUser created successfully"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
