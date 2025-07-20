import logging
from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message
from sheets.func_get import post_match_for_get
from aiogram.enums.parse_mode import ParseMode
from bot.create_bot import ADMINS_ID, bot

user_router = Router()

@user_router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer(f'Привет {message.from_user.first_name}')

@user_router.message(Command('get'))
async def get_data(message: Message):
    try:
        matches = post_match_for_get()  # Эта функция уже сама всё проверяет
        if matches:
            for _, match_data in matches:
                text = f"Время начала: {_} \n<b>{match_data['Команда 1']}</b> {match_data['Счет 1']} : {match_data['Счет 2']} <b>{match_data['Команда 2']}</b>"
                parse_mode = ParseMode.HTML
                await message.answer(text=text, parse_mode=parse_mode)
                logging.info(f"📨 Отправлено сообщение в чат {message.chat.id} пользователю {message.from_user.id}: {text}")
        else:
            await message.answer(text="Сегодня нет матчей")
    except Exception as e:
            logging.error("❌ Ошибка при проверке или отправке матчей:", exc_info=True)

@user_router.message()
async def send_message_to_admins(message: Message):
    try:
        text_from_user = (
        f"Пользователь: {message.from_user.first_name} {message.from_user.last_name}\n"
        f"id: {message.from_user.id}\n"
        f"link: @{message.from_user.username}\n"
        "Отправил сообщение:\n"
        f"{message.text}"
        )
        
        for admin_id in ADMINS_ID:
            await bot.send_message(chat_id=admin_id, text=text_from_user)
    except TypeError:
        await message.answer("Nice try!")
