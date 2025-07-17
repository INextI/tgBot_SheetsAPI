from datetime import datetime
import logging
from .sheets_api import get_data

def get_matches_today(matches: dict) -> list[tuple[str, dict]]:
    now = datetime.now()
    today = now.date()
    matches_today = []

    for time_str, data in matches.items():
        dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M")

        if dt.date() == today:
            try:
                matches_today.append((time_str, data))
            except ValueError:
                continue

    return matches_today

def post_match_for_get():
    try:
        matches = get_data()
        matches_today = get_matches_today(matches)
        logging.info("Вызвана post_match_for_get() с помощью команды /get")
        return matches_today
    except ValueError as e:
        logging.error(f"Ошибка при попытке получить все матчи дня (/get): {e}")
