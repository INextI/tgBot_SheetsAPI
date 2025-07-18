import logging
from aiogram import Bot, Dispatcher
from config import TOKEN
from config import ADMIN_ID, ADMIN2_ID

ADMINS_ID = [int(ADMIN_ID), int(ADMIN2_ID)]

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def start_bot():
    try:
        for id in ADMINS_ID:
            await bot.send_message(chat_id=int(id), text="Бот запущен")
    except Exception as e:
        logging.error(f"Ошибка в start_bot(): {e}")

async def stop_bot():
    try:
        for id in ADMINS_ID:
            await bot.send_message(chat_id=int(id), text="Бот остановлен")
    except Exception as e:
        logging.error(f"Ошибка в stop_bot(): {e}")
        