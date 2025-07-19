from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_inline_menu_for_change_bo():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Установить BO7", callback_data="BO7")],
        [InlineKeyboardButton(text="Установить BO9", callback_data="BO9")],
        [InlineKeyboardButton(text="Установить BO13", callback_data="BO13")]
    ])
    return keyboard

def get_main_menu():
    main_keyboard = [
        [KeyboardButton(text='⚙️ Настройка BO_N')],
        [KeyboardButton(text='📄 Поменять листы')],
        [KeyboardButton(text='⏱️ Поменять задержку')],
        [KeyboardButton(text='📃 Последние логи')],
        ]
    menu = ReplyKeyboardMarkup(keyboard=main_keyboard, 
                               resize_keyboard=True, 
                               one_time_keyboard=False,
                               input_field_placeholder='Выберите действие'
                               )
    return menu

def get_bo_menu():
    bo_keyboard = [
        [KeyboardButton(text="Установить BO7")],
        [KeyboardButton(text="Установить BO9")],
        [KeyboardButton(text="Установить BO13")],
        [KeyboardButton(text="⬅️ Назад")],
    ]

    bo_menu = ReplyKeyboardMarkup(keyboard=bo_keyboard,
                                  resize_keyboard= True,
                                  one_time_keyboard= False,
                                  input_field_placeholder='Выберите BO',
                                  )
    
    return bo_menu