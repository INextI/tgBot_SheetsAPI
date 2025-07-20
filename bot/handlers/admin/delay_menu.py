import config
from aiogram import F
from . import admin_router
from aiogram.types import Message
from bot.decorators import admin_only
from bot.create_bot import ADMINS_ID, bot
from bot.menu.admin import get_delay_menu, get_main_menu

@admin_router.message(F.text == '⏱️ Поменять задержку')
@admin_only
async def open_delay_menu(message: Message):
    await message.answer('Delay меню', reply_markup=get_delay_menu())

@admin_router.message(F.text == 'Без задержки')
@admin_only
async def remove_delay(message: Message):
    config.DELAY = 0
    for admin_id in ADMINS_ID:
        await bot.send_message(chat_id=admin_id, text='Установлено без задержки')

@admin_router.message(F.text == '1 мин')
@admin_only
async def remove_delay(message: Message):
    config.DELAY = 60
    for admin_id in ADMINS_ID:
        await bot.send_message(chat_id=admin_id, text='Установлена задержка 1 мин')

@admin_router.message(F.text == '3 мин')
@admin_only
async def remove_delay(message: Message):
    config.DELAY = 180
    for admin_id in ADMINS_ID:
        await bot.send_message(chat_id=admin_id, text='Установлена задержка 3 мин')

@admin_router.message(F.text == '5 мин')
@admin_only
async def remove_delay(message: Message):
    config.DELAY = 300
    for admin_id in ADMINS_ID:
        await bot.send_message(chat_id=admin_id, text='Установлена задержка 5 мин')

@admin_router.message(F.text == '7 мин')
@admin_only
async def remove_delay(message: Message):
    config.DELAY = 420
    for admin_id in ADMINS_ID:
        await bot.send_message(chat_id=admin_id, text='Установлена задержка 7 мин')

@admin_router.message(F.text == '10 мин')
@admin_only
async def remove_delay(message: Message):
    config.DELAY = 600
    for admin_id in ADMINS_ID:
        await bot.send_message(chat_id=admin_id, text='Установлена задержка 10 мин')