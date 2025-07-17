import gspread
from google.oauth2.service_account import Credentials
import re
from datetime import datetime
from config import POSTED_FILE, HASHES, JSON_DUMP, SHEET_ID, TIME_ZONE
import config
import json
from collections import OrderedDict
import logging
from .utils import get_sheet_hash, to_datetime

scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]

creds = Credentials.from_service_account_file("credentials.json", scopes= scopes)
client = gspread.authorize(creds)


def check_updated_sheets(sheet_ids: list[int]) -> list[int]:
    current_hashes = {}
    changed_sheets = []

    # Получаем текущие хеши
    for n in sheet_ids:
        try:
            sheet = client.open_by_key(SHEET_ID).get_worksheet(n)
            data = sheet.get_all_values()
            current_hashes[str(n)] = get_sheet_hash(data)
        except Exception as e:
            logging.error(f"Ошибка при получение хеша для листа {n} : {e}")
            continue

    # Загружаем предыдущие хеши
    try:
        with open(HASHES, 'r', encoding='utf-8') as f:
            old_hashes = json.load(f)
    except FileNotFoundError:
        old_hashes = {}
        with open(HASHES, 'w', encoding='utf-8') as f:
            json.dump(old_hashes, f, indent=4, ensure_ascii=False)

    # Проверяем изменения
    for sheet_id_str, curr_hash in current_hashes.items():
        if old_hashes.get(sheet_id_str) != curr_hash:
            changed_sheets.append(int(sheet_id_str))

    # Сохраняем новые хеши
    with open(HASHES, 'w', encoding='utf-8') as f:
        json.dump(current_hashes, f, indent=4, ensure_ascii=False)

    if not changed_sheets:
        return None

    return changed_sheets


def get_data() -> dict:
    pattern_date = re.compile(r"\b([1-9]|[12][0-9]|3[01])\s+(января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря)\b")
    pattern_team = re.compile(r"^Команда\s+\d+$")

    matches = {}
    for n in range(9,10):
        try:
            sheet = client.open_by_key(SHEET_ID).get_worksheet(n)
            data = sheet.get_all_values()
        except Exception as e:
            logging.error("Ошибка при получение значение из get_data() : {e}")

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


def get_data_from_sheet(sheet_id: int) -> dict:
    pattern_date = re.compile(r"\b([1-9]|[12][0-9]|3[01])\s+(января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря)\b")
    pattern_team = re.compile(r"^Команда\s+\d+$")

    matches = {}
    try:
        sheet = client.open_by_key(SHEET_ID).get_worksheet(sheet_id)
        data = sheet.get_all_values()
    except Exception as e:
        logging.error("Ошибка при получение значение из get_data_from_sheet() : {e}")
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

def get_finished_matches_today_unposted(matches: dict) -> list[tuple[str, dict]]:
    now = datetime.now(TIME_ZONE)  # московское время
    today = now.date()
    finished = []
    count_today_matches = 0
    today_matches = []

    try:
        with open(POSTED_FILE, 'r', encoding='utf-8') as f:
            posted = set(json.load(f))
    except FileNotFoundError:
        posted = set()

    for time_str, data in matches.items():
        dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        dt = dt.replace(tzinfo=TIME_ZONE)  # делаем дату тоже aware

        if dt.date() == today and time_str not in posted: #and dt <= now
            try:
                score1 = int(data['Счет 1'])
                score2 = int(data['Счет 2'])
                if score1 == config.BO_N or score2 == config.BO_N:
                    finished.append((time_str, data))
            except ValueError:
                continue
        if dt.date() == today:
            today_matches.append((time_str, data))
            count_today_matches += 1

    return finished, today_matches, count_today_matches

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


def mark_matches_as_posted(match_keys: list[str]):
    try:
        with open(POSTED_FILE, 'r', encoding='utf-8') as f:
            posted = set(json.load(f))
    except FileNotFoundError:
        posted = set()

    posted.update(match_keys)

    with open(POSTED_FILE, 'w', encoding='utf-8') as f:
        json.dump(sorted(posted), f, indent=4, ensure_ascii=False)


def update():
    updated_sheets = check_updated_sheets([9]) #[3,4,5] [7]
    if updated_sheets == None:
        return False
    if len(updated_sheets) == 1:
        data = get_data_from_sheet(updated_sheets[0])
    
    else:
        data = get_data()
    return data


def post_match():
    matches = update()
    if matches:
        logging.info("Таблица обновилась")
        new_matches, today_matches, count_today_matches = get_finished_matches_today_unposted(matches)
        if new_matches:
            logging.info("Есть завершенный матч")
            return new_matches, today_matches, count_today_matches
        else:
            logging.info("Матч ещё не завершён")
            return False  
    else:
        return False
    
def post_match_for_get():
    try:
        matches = get_data()
        matches_today = get_matches_today(matches)
        logging.info("Вызвана post_match_for_get() с помощью команды /get")
        return matches_today
    except ValueError as e:
        logging.error(f"Ошибка при попытке получить все матчи дня (/get): {e}")