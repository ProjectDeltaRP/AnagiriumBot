from google.oauth2 import service_account
from googleapiclient.discovery import build

from bot_init import bot
from config import SERVICE_ACCOUNT_INFO, SPREADSHEET_ID_GOOGLE

RANGE_NAME = "Игроки (включая администрацию)!B2:C"

# Создаем credentials из словаря
credentials = service_account.Credentials.from_service_account_info(
    SERVICE_ACCOUNT_INFO,
    scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
)

service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

@bot.slash_command(description="Показать таблицу Игроки (Discord ID и Роблокс профиль)")
async def players(inter):
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID_GOOGLE, range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        await inter.response.send_message("Таблица пуста или данные не найдены.")
        return

    msg_lines = []
    for row in values:
        discord_id = row[0] if len(row) > 0 else "Нет данных"
        roblox_profile = row[1] if len(row) > 1 else "Нет данных"
        msg_lines.append(f"**Discord ID:** {discord_id} — **Роблокс профиль:** {roblox_profile}")

    message = "\n".join(msg_lines)
    if len(message) > 1900:
        message = message[:1900] + "\n..."

    await inter.response.send_message(message)
