import logging
import asyncio
import random
from ..create_bot import bot
from sheets.main import post_match
from sheets.posted import mark_matches_as_posted
from config import COUNT_MATHCES, CHANNEL_ID
from aiogram.enums.parse_mode import ParseMode


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