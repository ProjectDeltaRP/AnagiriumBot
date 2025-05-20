"""
Модуль для запуска бота.
"""

from bot_init import bot
from config import DISCORD_TOKEN
from commands import general_commands
from events import on_ready


if __name__ == "__main__":
    if DISCORD_TOKEN == "NULL":
        print("[ERROR] Not DISCORD_KEY. Programm Dev-bot shutdown!!")
    else:
        bot.run(DISCORD_TOKEN)
