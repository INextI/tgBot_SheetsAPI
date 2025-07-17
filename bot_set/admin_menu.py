from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_admin_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Установить BO7", callback_data="BO7")],
        [InlineKeyboardButton(text="Установить BO9", callback_data="BO9")],
        [InlineKeyboardButton(text="Установить BO13", callback_data="BO13")]
    ])
    return keyboard
