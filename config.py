"""
Этот модуль содержит все основные конфигурации Dev-bot.
"""

import os
from dotenv import load_dotenv

# Загрузка переменных из .env
load_dotenv()

def get_env_variable(name: str, default: str = "NULL") -> str:
    """
    Функция для безопасного получения переменных окружения.
    Если переменная не найдена, возвращает значение по умолчанию.
    """
    value = os.getenv(name)
    if not value:
        print(f"Предупреждение: {name} не найден в файле .env. "
              f"Используется значение по умолчанию: {default}"
        )
        return default
    return value

# Получение переменных из окружения
DISCORD_TOKEN = get_env_variable("DISCORD_TOKEN")