import os

from dotenv import load_dotenv
from zoneinfo import ZoneInfo
from pathlib import Path
from datetime import datetime

load_dotenv()

BASE_DIR = Path(__file__).parent

TIME_ZONE = ZoneInfo("Europe/Moscow")

START_TIME = datetime.now(TIME_ZONE)

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

LOG_FILE = BASE_DIR / 'logs/bot.log'

BO_N = 4

DELAY = 300

SHEET_LIST = [10] #[3,4,5] [7] , [9]

JSON_DIR = BASE_DIR / 'json_db'

JSON_DUMP = JSON_DIR / "json_dump.json"
HASHES = JSON_DIR / "sheet_hashes.json"
POSTED_FILE = JSON_DIR / "posted_matches.json"

TOKEN = os.getenv("TOKEN")

CHANNEL_ID = os.getenv("CHANNEL_ID")
SHEET_ID = os.getenv("SHEET_ID")
ADMIN_ID = os.getenv('ADMIN_ID')
ADMIN2_ID = os.getenv('ADMIN2_ID')

# from test import token
# TOKEN = token