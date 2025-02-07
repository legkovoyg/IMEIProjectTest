import logging
import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import os
from dotenv import load_dotenv

load_dotenv()
# Замените на токен вашего бота
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
print(API_TOKEN)
# Настройка логирования
logging.basicConfig(level=logging.INFO)

def is_valid_imei(imei: str) -> bool:
    """
    Проверяет, что IMEI состоит из 15 цифр и проходит проверку алгоритмом Луна.
    """
    if len(imei) != 15 or not imei.isdigit():
        return False

    total = 0
    reverse_digits = imei[::-1]
    for i, digit_char in enumerate(reverse_digits):
        digit = int(digit_char)
        if i % 2 == 1:  # каждую вторую цифру удваиваем
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return total % 10 == 0

async def start_handler(message: types.Message):
    """
    Обработчик команды /start.
    """
    await message.answer(
        "Привет! Это бот для проверки IMEI! проверить IMEI, напиши команду /imei "
    )

async def imei_handler(message: types.Message):
    """
    Обрабатывает текстовые сообщения, интерпретируя их как IMEI.
    """
    imei = message.text.strip()
    if not imei.isdigit() or len(imei) != 15:
        await message.answer("Пожалуйста, отправьте корректный IMEI (15 цифр).")
        return
    if is_valid_imei(imei):
        response = f"IMEI {imei} действительный (проверка Луна)."
    else:
        response = f"IMEI {imei} недействительный (не проходит проверку Луна)."


    await message.answer(response)

async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()
    dp.message.register(start_handler, Command("start"))
    dp.message.register(imei_handler)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
