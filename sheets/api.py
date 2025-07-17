import gspread
from google.oauth2.service_account import Credentials
from config import SHEET_ID
from typing import Any, List

scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]

creds = Credentials.from_service_account_file("credentials.json", scopes= scopes)
client = gspread.authorize(creds)


def sheet_request(num_of_sheet: int) -> List[List[Any]]:
    sheet = client.open_by_key(SHEET_ID).get_worksheet(num_of_sheet)
    data = sheet.get_all_values()
    return data