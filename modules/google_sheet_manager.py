from google.oauth2 import service_account
from googleapiclient.discovery import build

class GoogleSheetManager:
    def __init__(self, service_account_info: dict, spreadsheet_id: str, scopes=None):
        if scopes is None:
            scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']

        self.credentials = service_account.Credentials.from_service_account_info(
            service_account_info,
            scopes=scopes
        )
        self.service = build('sheets', 'v4', credentials=self.credentials)
        self.spreadsheet_id = spreadsheet_id
        self.sheet = self.service.spreadsheets()

    def get_values(self, range_name: str):
        """
        Получить значения из указанного диапазона таблицы.
        Возвращает список списков (строк).
        """
        result = self.sheet.values().get(
            spreadsheetId=self.spreadsheet_id,
            range=range_name
        ).execute()
        return result.get('values', [])

    def get_dicts(self, range_name: str):
        """
        Получить данные из таблицы в виде списка словарей,
        где ключи — это заголовки из первой строки диапазона,
        а значения — соответствующие ячейки.
        """
        values = self.get_values(range_name)
        if not values or len(values) < 2:
            return []

        headers = [h.strip() for h in values[0]]
        data_rows = values[1:]
        result = []
        for row in data_rows:
            # Заполняем отсутствующие ячейки пустыми строками
            row_extended = row + [''] * (len(headers) - len(row))
            row_dict = dict(zip(headers, row_extended))
            result.append(row_dict)
        return result

    def get_roblox_profile_by_discord_id(self, discord_id: str, range_name: str):
        data = self.get_dicts(range_name)
        for row in data:
            if row.get('Дискорд ID') == discord_id:
                return row.get('Роблокс профиль', None)
        return None

    def get_discord_id_by_roblox_profile(self, roblox_profile: str, range_name: str):
        data = self.get_dicts(range_name)
        for row in data:
            if row.get('Роблокс профиль') == roblox_profile:
                return row.get('Дискорд ID', None)
        return None
