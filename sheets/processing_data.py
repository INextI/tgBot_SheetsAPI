import re
from datetime import datetime
from config import JSON_DUMP
import json
from collections import OrderedDict
import logging
from .utils import to_datetime
from .api import sheet_request


def get_data(nums_of_sheet: list[int]) -> dict:
    pattern_date = re.compile(r"\b([1-9]|[12][0-9]|3[01])\s+(января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря)\b")
    pattern_team = re.compile(r"^Команда\s+\d+$")

    matches = {}
    for sheet_num in nums_of_sheet:
        try:
            data = sheet_request(sheet_num)
        except Exception as e:
            logging.error(f"Ошибка при получение значение из get_data(), лист {sheet_num} : {e}")

        for i, row in enumerate(data):
            if pattern_date.match(row[0]):
                j=i+1
                while j<len(data) and not pattern_date.match(data[j][0]):
                    if pattern_team.match(data[j][0]):
                        j+=1
                        continue
                    if not data[j][0]:
                        j+=1
                        continue
                    
                    if not data[j][2]:
                        j+=1
                        continue
                    #print(row[0], data[j][2])
                    dt = to_datetime(row[0], data[j][2])
                    matches[dt.strftime('%Y-%m-%d %H:%M')] = {
                        'Команда 1': data[j][0],
                        'Счет 1': data[j][1],
                        'Время': data[j][2],
                        'Счет 2': data[j][3],
                        'Команда 2': data[j][4]
                    }
                    j+=1
    matches = OrderedDict(
    sorted(
        matches.items(),
        key=lambda item: datetime.strptime(item[0], '%Y-%m-%d %H:%M')
    )
    )
    with open(JSON_DUMP, 'w', encoding='utf-8') as f:
        json.dump(matches, f, indent=4, ensure_ascii=False)
    return matches