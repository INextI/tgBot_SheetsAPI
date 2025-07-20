import config
import logging
from aiogram import Bot, Dispatcher
from config import TOKEN
from config import ADMIN_ID, ADMIN2_ID
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

class SheetState(StatesGroup):
    waiting_for_sheet_input = State()

ADMINS_ID = [int(ADMIN_ID), int(ADMIN2_ID)]

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

async def start_bot():
    try:
        text = ("Бот запущен\n\n"
                "Установлены значения по умолчанию:\n"
                f"Задержка: {config.DELAY // 60} мин\n"
                f"Листы табл. для парсинга: {config.SHEET_LIST}\n"
                f"Количество побед в матче до: {config.BO_N}\n"
                )
        for id in ADMINS_ID:
            await bot.send_message(chat_id=int(id), text=text)
    except Exception as e:
        logging.error(f"Ошибка в start_bot(): {e}")

async def stop_bot():
    try:
        for id in ADMINS_ID:
            await bot.send_message(chat_id=int(id), text="Бот остановлен")
    except Exception as e:
        logging.error(f"Ошибка в stop_bot(): {e}")
        