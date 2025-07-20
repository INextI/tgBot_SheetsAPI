from aiogram import F
from aiogram.types import Message
from bot.menu.admin import get_main_menu
from aiogram.filters.command import Command
from bot.decorators import admin_only
from bot.services.get_logs import get_logs
from . import admin_router

@admin_router.message(Command('menu'))
@admin_only
async def admin_menu(message: Message):
    await message.answer("Админ-меню:", reply_markup=get_main_menu())

@admin_router.message(F.text == '⬅️ Назад')
@admin_only
async def open_bo_menu(message: Message):
    await message.answer("Вы вернулись в админ-меню", reply_markup=get_main_menu())

@admin_router.message(F.text == '📃 Последние логи')
@admin_only
async def logs(message: Message):
    log = get_logs()
    msg = ''
    for line in log:
        msg += line
    await message.answer(msg)