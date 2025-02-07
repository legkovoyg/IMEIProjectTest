from pydantic import BaseModel

# Модель для запроса на проверку токена
class TokenRequest(BaseModel):
    token: str

class TgRequest(BaseModel):
    telegram_id: str


# Модель для ответа при проверке токена
class TokenResponse(BaseModel):
    valid: bool
    username: str | None = None

# Модель для ответа при проверке tg
class TgResponse(BaseModel):
    valid: bool
    username: str | None = None

# Модель для создания нового пользователя (таблица users)
class UserCreate(BaseModel):
    username: str
    token: str

# Модель для создания новой записи в белом списке Telegram-пользователей (таблица telegram_whitelist)
class TelegramWhitelistCreate(BaseModel):
    telegram_id: str
    username: str
