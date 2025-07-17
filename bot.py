import asyncio
from config import TOKEN, CHANNEL_ID, COUNT_MATHCES, ADMIN_ID
import config
from aiogram import Bot, Dispatcher, types
from sheets.processing_data import post_match
from sheets.posted import mark_matches_as_posted
from sheets.func_get import post_match_for_get
from aiogram.filters.command import Command
from aiogram.enums.parse_mode import ParseMode
import logging
import random
from logs.logger_config import setup_logger
from bot_set.admin_menu import get_admin_menu

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"Привет {message.from_user.first_name}")

@dp.message(Command("get"))
async def get_data(message: types.Message):
    try:
        matches = post_match_for_get()  # Эта функция уже сама всё проверяет
        if matches:
            for _, match_data in matches:
                text = f"Время начала: {_} \n<b>{match_data['Команда 1']}</b> {match_data['Счет 1']} : {match_data['Счет 2']} <b>{match_data['Команда 2']}</b>"
                parse_mode = ParseMode.HTML
                await bot.send_message(chat_id=message.chat.id, text=text, parse_mode=parse_mode)
                logging.info(f"📨 Отправлено сообщение в чат {message.chat.id} пользователю {message.from_user.id}: {text}")
                #mark_matches_as_posted([t for t, _ in matches])
        else:
            await bot.send_message(chat_id=message.chat.id, text="Сегодня нет матчей")
    except Exception as e:
            logging.error("❌ Ошибка при проверке или отправке матчей:", exc_info=True)

@dp.message(Command("menu"))
async def admin_menu(message: types.Message):
    if message.from_user.id == int(ADMIN_ID):
        await message.answer("Админ-меню:", reply_markup=get_admin_menu())
    else:
        await message.answer("У тебя нет доступа к этому меню.")

@dp.callback_query()
async def handle_admin_callbacks(callback: types.CallbackQuery):
    if callback.from_user.id != int(ADMIN_ID):
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

@dp.message()
async def echo(message: types.Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")

# задача, проверяющая матчи каждые N секунд

async def match_watcher():
    while True:
        try:
            result = post_match() # Эта функция уже сама всё проверяет
            if result:
                matches, today_matches, count_today_matches = result
                for date, match_data in matches:
                    for i in range(len(today_matches)):
                        time_date, _ = today_matches[i]

                        if time_date == date:
                            if count_today_matches == i+1:
                                text_match = COUNT_MATHCES['финал'][random.choice([1,2])]
                            elif i >= 5:
                                text_match = "Матч"
                            else:
                                text_match = COUNT_MATHCES[i+1]

                            text = f"🏆 {text_match} завершён: \n\n<b>{match_data['Команда 1']}</b> <span class=\"tg-spoiler\"> {match_data['Счет 1']} </span>:<span class=\"tg-spoiler\"> {match_data['Счет 2']} </span> <b>{match_data['Команда 2']}</b>"
                            parse_mode = ParseMode.HTML
                            await asyncio.sleep(300) # Задержка отправки
                            await bot.send_message(CHANNEL_ID, text=text, parse_mode=parse_mode)
                            logging.info(f"📨 Отправлено сообщение: {text} в канал {CHANNEL_ID}")
                            mark_matches_as_posted([t for t, _ in matches])
        except Exception as e:
            logging.error("❌ Ошибка при проверке или отправке матчей:", exc_info=True)
        await asyncio.sleep(120)  # Проверяем раз в 2 минуты (можно изменить)

async def main():
    await asyncio.gather(
        match_watcher(),
        dp.start_polling(bot)
    )

if __name__ == "__main__":
    try:
        setup_logger()
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")