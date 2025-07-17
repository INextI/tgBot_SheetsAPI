import os

from dotenv import load_dotenv
from zoneinfo import ZoneInfo

load_dotenv()

TIME_ZONE = ZoneInfo("Europe/Moscow")

MONTHS_RU = {
    'января': 'January',
    'февраля': 'February',
    'марта': 'March',
    'апреля': 'April',
    'мая': 'May',
    'июня': 'June',
    'июля': 'July',
    'августа': 'August',
    'сентября': 'September',
    'октября': 'October',
    'ноября': 'November',
    'декабря': 'December',
}

COUNT_MATHCES = {
    1: 'Первый матч',
    2: 'Второй матч',
    3: 'Третий матч',
    4: 'Четвёртый матч',
    5: 'Пятый матч',
    'финал' : {
        1: 'Финальный матч сегодняшенего дня',
        2: 'Последний матч на сегодня',
    }

}

BO_N = 5

JSON_DUMP = "json_db/json_dump.json"
HASHES = "json_db/sheet_hashes.json"
POSTED_FILE = "json_db/posted_matches.json"

TOKEN = os.getenv("TOKEN")

CHANNEL_ID = os.getenv("CHANNEL_ID")
SHEET_ID = os.getenv("SHEET_ID")
ADMIN_ID = os.getenv('ADMIN_ID')