import logging
import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DB_SERVICE_URL = "http://db_service:8002"
API_SERVICE_URL = "http://api_service:8001"
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def is_valid_imei_local_check(imei: str) -> bool:
    if len(imei) != 15 or not imei.isdigit():
        return False

    total = 0
    reverse_digits = imei[::-1]
    for i, digit_char in enumerate(reverse_digits):
        digit = int(digit_char)
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit

    return (total % 10 == 0)

def check_whitelist(telegram_id: int, username: str) -> bool:
    """
    Проверяет через db_service, находится ли Telegram-пользователь в вайтлисте.
    Возвращает True, если пользователь есть в вайтлисте, иначе False.
    """
    url = f"{DB_SERVICE_URL}/telegram-whitelist/check"
    payload = {
        "telegram_id": str(telegram_id),
    }
    logging.info(f'url : {url}, payload : {payload}')
    try:
        resp = requests.post(url, json=payload)
        logging.info(f"resp : {resp.text}")
        if resp.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        logging.error(f"Ошибка при проверке вайтлиста: {e}")
        return False

def check_imei_api(imei: str) -> str:
    url = f"{API_SERVICE_URL}/api/check-imei"
    payload = {"imei": imei}
    try:
        resp = requests.post(url, json=payload)
        if resp.status_code == 200:
            return resp.text
        else:
            return f"Ошибка от API-сервиса, статус {resp.status_code}: {resp.text}"
    except Exception as e:
        logging.error(f"Ошибка при запросе к api_service: {e}")
        return f"Ошибка при запросе к API: {str(e)}"

async def start_handler(message: types.Message):
    await message.answer(
        "Привет! Это бот для проверки IMEI.\n"
        "Отправь 15-значный IMEI, и я проверю:\n"
        "1) Есть ли ты в вайтлисте?\n"
        "2) Проходит ли IMEI локальную проверку алгоритмом Луна?\n"
        "3) Если всё ок — сделаю запрос к API-сервису.\n"
    )

async def imei_handler(message: types.Message):

    telegram_id = message.from_user.id
    username = message.from_user.username

    logging.info(f"Получено сообщение от Telegram ID: {telegram_id}, Username: {username}")
    in_whitelist = check_whitelist(telegram_id, username)
    if not in_whitelist:
        await message.answer("Извините, вас нет в вайтлисте. Обратитесь к администратору.")
        return

    imei = message.text.strip()
    if not imei.isdigit() or len(imei) != 15:
        await message.answer("Пожалуйста, отправьте корректный IMEI (15 цифр).")
        return

    if not is_valid_imei_local_check(imei):
        await message.answer(f"IMEI {imei} не проходит проверку алгоритмом Луна (Luhn).")
        return

    api_response = check_imei_api(imei)
    await message.answer(f"Результат от API-сервиса:\n{api_response}")

async def main():
    dp.message.register(start_handler, Command("start"))
    dp.message.register(imei_handler)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
