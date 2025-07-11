"""
Этот модуль инициализирует бота для работы с Discord.
Настроены необходимые параметры для запуска и обработки команд.
"""

import disnake
from disnake.ext import commands
from modules.google_sheet_manager import GoogleSheetManager

from config import GUILD_ID, SERVICE_ACCOUNT_INFO, SPREADSHEET_ID_GOOGLE

intents = disnake.Intents.all()
intents.message_content = True
intents.members = True
intents.voice_states = True
intents.guilds = True


bot = commands.Bot(
    command_prefix="!",
    help_command=None,
    intents=intents,
    sync_commands=True,
    test_guilds=[GUILD_ID]
)

sheet_manager = GoogleSheetManager(SERVICE_ACCOUNT_INFO, SPREADSHEET_ID_GOOGLE)