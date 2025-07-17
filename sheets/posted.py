import json
import config
from datetime import datetime
from config import POSTED_FILE, TIME_ZONE

def mark_matches_as_posted(match_keys: list[str]):
    try:
        with open(POSTED_FILE, 'r', encoding='utf-8') as f:
            posted = set(json.load(f))
    except FileNotFoundError:
        posted = set()

    posted.update(match_keys)

    with open(POSTED_FILE, 'w', encoding='utf-8') as f:
        json.dump(sorted(posted), f, indent=4, ensure_ascii=False)


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