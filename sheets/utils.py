from config import MONTHS_RU
from datetime import datetime

def to_datetime(date: str, time: str) -> datetime:
    current_year = datetime.now().year
    try:
        day, month_rus = date.strip().split()
        month_eng = MONTHS_RU[month_rus]
        datetime_str = f"{day} {month_eng} {current_year} {time.strip()}"
        return datetime.strptime(datetime_str, "%d %B %Y %H:%M")

    except KeyError:
        raise ValueError(f"Месяц не распознан: {month_rus}")
    except ValueError as ve:
        raise ValueError(f"Ошибка парсинга времени: {ve}")
    