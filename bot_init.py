"""
Этот модуль инициализирует бота для работы с Discord.
Настроены необходимые параметры для запуска и обработки команд.
"""
import disnake
from disnake.ext import commands

intents = disnake.Intents.all()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    help_command=None,
    intents=intents
)
