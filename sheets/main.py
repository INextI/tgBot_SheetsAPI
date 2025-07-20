import logging
from config import SHEET_LIST
from .hashes import check_updated_sheets
from .processing_data import get_data
from .posted import get_finished_matches_today_unposted

def update():
    updated_sheets = check_updated_sheets(SHEET_LIST)
    if updated_sheets == None:
        return False
    data = get_data(SHEET_LIST)
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