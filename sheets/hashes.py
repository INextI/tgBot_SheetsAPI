import logging
import hashlib
import json
from config import HASHES
from .api import sheet_request

def get_sheet_hash(data: list[list[str]]) -> str:
    flat_data = ''.join(''.join(row) for row in data)
    return hashlib.md5(flat_data.encode('utf-8')).hexdigest()


def check_updated_sheets(sheet_nums: list[int]) -> list[int]:
    current_hashes = {}
    changed_sheets = []

    # Получаем текущие хеши
    for sheet_num in sheet_nums:
        try:
            data = sheet_request(sheet_num)
            current_hashes[str(sheet_num)] = get_sheet_hash(data)
        except Exception as e:
            logging.error(f"Ошибка при получение хеша для листа {sheet_num} : {e}")
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