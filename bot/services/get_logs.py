from config import LOG_FILE
from collections import deque

def get_logs() -> list[str]:
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        last_lines = deque(f, maxlen= 20)
    logs = []
    for line in last_lines:
        logs.append(line)
    return logs