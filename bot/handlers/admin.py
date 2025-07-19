import config
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command
from bot.menu.admin import get_main_menu, get_bo_menu
from bot.decorators import admin_only
from bot.create_bot import ADMINS_ID, bot

admin_router = Router()

@admin_router.message(Command('menu'))
@admin_only
async def admin_menu(message: Message):
    await message.answer("Админ-меню:", reply_markup=get_main_menu())

@admin_router.message(F.text == '⚙️ Настройка BO_N')
@admin_only
async def open_bo_menu(message: Message):
    await message.answer("BO меню", reply_markup=get_bo_menu())

@admin_router.message(F.text == '⬅️ Назад')
@admin_only
async def open_bo_menu(message: Message):
    await message.answer("Вы вернулись в админ-меню", reply_markup=get_main_menu())

@admin_router.message(F.text == 'Установить BO7')
@admin_only
async def set_bo7(message: Message):
    config.BO_N = 4
    for admin_id in ADMINS_ID:
        await bot.send_message(admin_id, text='Установлено BO7 (до 4 побед)')

@admin_router.message(F.text == 'Установить BO9')
@admin_only
async def set_bo9(message: Message):
    config.BO_N = 5
    for admin_id in ADMINS_ID:
        await bot.send_message(admin_id, text='Установлено BO9 (до 5 побед)')

@admin_router.message(F.text == 'Установить BO13')
@admin_only
async def set_bo13(message: Message):
    config.BO_N = 7
    for admin_id in ADMINS_ID:
        await bot.send_message(admin_id, text='Установлено BO13 (до 7 побед)')
    

     