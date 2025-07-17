# logger_config.py

import logging
from datetime import datetime
from zoneinfo import ZoneInfo
from config import TIME_ZONE

class MoscowFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, TIME_ZONE)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.isoformat()

def setup_logger():
    # Создаем кастомный форматтер
    formatter = MoscowFormatter(
        fmt="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S [MSK]"
    )

    # Настраиваем обработчики
    file_handler = logging.FileHandler("logs/bot.log", encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Очищаем старые обработчики (если setup_logger вызывается повторно)
    root_logger = logging.getLogger()
    root_logger.handlers = []

    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

