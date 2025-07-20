import config
from aiogram import F
from . import admin_router
from bot.decorators import admin_only
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.create_bot import ADMINS_ID, bot, SheetState

@admin_router.message(F.text == '📄 Поменять листы')
@admin_only
async def change_lists(message: Message, state: FSMContext):
    await message.answer("Введите листы через запятую (например: 4, 5, 6):")
    await state.set_state(SheetState.waiting_for_sheet_input)

@admin_router.message(SheetState.waiting_for_sheet_input)
@admin_only
async def handle_sheet_input(message: Message, state: FSMContext):
    input_text = message.text.strip()

    try:
        sheet_list = [int(num.strip()) for num in input_text.split(',')]
        for admin_id in ADMINS_ID:
            await bot.send_message(chat_id=admin_id, text=f'Установлены таблицы для парсинга с номерами {sheet_list}')
        
        config.SHEET_LIST = sheet_list
        await state.clear()
    except ValueError:
        await message.answer("Ошибка: введите только числа, разделённые запятой.")
