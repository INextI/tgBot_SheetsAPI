from pathlib import Path
from config import JSON_DIR

def create_jsondb_dir():
    JSON_DIR.mkdir(exist_ok=True)