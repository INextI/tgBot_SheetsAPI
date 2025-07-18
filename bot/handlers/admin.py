import config
from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command
from bot.menu.admin import get_menu, get_inline_menu_for_change_bo
from bot.create_bot import ADMINS_ID

admin_router = Router()


from bot.menu.admin import get_menu

@admin_router.message(Command('lol'))
async def test(message: Message):
    await message.answer('lol', reply_markup=get_menu())

@admin_router.message(Command("menu"))
async def admin_menu(message: Message):
    if message.from_user.id in ADMINS_ID:
        await message.answer("Админ-меню:", reply_markup=get_menu())
    else:
        await message.answer("У вас нет доступа к этому меню.")

@admin_router.callback_query()
async def handle_admin_callbacks(callback: CallbackQuery):
    if callback.from_user.id not in ADMINS_ID:
        await callback.answer("Нет доступа", show_alert=True)
        return

    if callback.data == "BO7":
        config.BO_N = 4
        await callback.answer("Установлено BO7, матч до 4 побед")

    if callback.data == "BO9":
        config.BO_N = 5
        await callback.answer("Установлено BO9, матч до 5 побед")
    elif callback.data == "BO13":
        config.BO_N = 7
        await callback.answer("Установлено BO13, матч до 7 побед")
