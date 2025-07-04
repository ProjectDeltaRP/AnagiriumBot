"""
Этот модуль содержит все основные конфигурации Dev-bot.
"""

import os

import disnake
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
        print(
            f"Предупреждение: {name} не найден в файле .env. "
            f"Используется значение по умолчанию: {default}"
        )
        return default
    return value


# Получение переменных из окружения
DISCORD_TOKEN = get_env_variable("DISCORD_TOKEN")
GIT_PAT_TOKEN = get_env_variable("GIT_PAT_TOKEN")
API_KEY_ROBLOX = get_env_variable("API_KEY_ROBLOX")

LOG_TECH_CHANNEL = 1374529148474622085  # ID канала с логами
BACKUP_CHANNEL_ID = 1374736085929820191 # ID канала для сохранения настроек в случае отключения
GUILD_ID = 1374389368315449477          # ID Discord сервера
SHUTDOWN_TIMER = 5 * 60 * 60 + 56       # Время 5ч 56мин, время работы бота, после чего будет рестарт
ONLINE_MEMBER_CHANNEL = 1388564716288344075 # Го. канал показывающий участников онлайн
ALL_MEMBER_CHANNEL = 1388564649489993728    # Гс. канал показывающий общее кол-во участников

AUTHOR = 'ProjectDeltaRP'
REPO = 'AnagiriumBot'

# Айди пользователей с полными правами ко всем командам бота
FULL_PERMISSION_USERS = [328502766622474240, 375256003723132938]


# Ключи айди ролей, для распределения доступов к командам (Взяты рандомные айди для примера)
ROLE_WHITELISTS = {
    # Ключи ID ролей для вайтлистов
    "super_head_project": [
        1374393293646860419, # [👑] Высшее руководство
    ],
    "head_project": [
        1387477629820735498, # [👑] Руководство
    ],
    "general_administrations": [
        1374465376548683930, # [🛡️] Игровая администрация
    ],
    "senior_admin": [
        1387464129668972594, # [🛡️] Ст. игровой администратор
    ],
    "middle_admin": [
        1387464129668972594, # [🛡️] Ст. игровой администратор
        1374465770926506076, # [🛡️] Игровой администратор
    ],
}

# Айди ролей дискорда
DEPARTMENT_ROLES = {
    "ad": {
        "group": 1375433339242025040,                   # ◀◀  [🗒️] Административная служба  ▶▶
        "ranks": {
            "control": 1375435641751339113,             # [🗒️] Контроль процедур
            "sector": 1375435639075373098,              # [🗒️] Секториальный проверяющий
            "director": 1375435632033267832,            # [🗒️] Директор зоны
        },
    },
    "sd": {
        "group": 1375432802564177981,                   # ◀◀  [🛡️] Служба безопасности  ▶▶
        "ranks": {
            "cadet": 1375436641430278227,               # [🛡️] Кадет службы безопасности
            "officer": 1375436645729435749,             # [🛡️] Офицер службы безопасности
            "bio_officer": 1375436637256941598,         # [🛡️] Офицер химико-биологической службы безопасности
            "qrf": 1375436644169158699,                 # [🛡️] Группа быстрого реагирования
            "head": 1375436639832375386,                # [🛡️] Глава службы безопасности
        },
    },
    "scd": {
        "group": 1375433025944289350,                   # ◀◀  [🥼] Научная служба  ▶▶
        "ranks": {
            "researcher": 1375437300065894492,          # [🥼] Исследователь
            "senior_researcher": 1375437304637952000,   # [🥼] Старший исследователь
            "pre_lead_researcher": 1375437307162918922, # [🥼] Ведущий исследователь
            "lead": 1375437301450149938,                # [🥼] Научный руководитель
        },
    },
    "ms": {
        "group": 1375433515365040178,                   # ◀◀  [🩺] Медицинская служба  ▶▶
        "ranks": {
            "nurse": 1375437378012975115,               # [🩺] Фельдшер
            "doctor": 1375437373663612938,              # [🩺] Врач
            "bio_specialist": 1375437371360804874,      # [🩺] Специалист по биологическим угрозам
        },
    },
}

GROUP_CHOICES = {
    36048024: "Административная служба",
    36048147: "Научная служба",
    36046821: "Служба безопасности",
    36048117: "Медицинская служба",
}

GROUP_COLORS = {
    36046821: disnake.Color.light_grey(),   # Служба безопасности — красный
    36048147: disnake.Color.green(),        # Научная служба — фиолетовый
    36048117: disnake.Color.purple(),       # Медицинская служба — синий
    36048024: disnake.Color.yellow(),       # Административная служба — зелёный
}
