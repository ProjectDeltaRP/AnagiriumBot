# 🤖 AnagiriumBot

## 👤 Автор:  
- Discord: **schrodinger71** (id:328502766622474240)
- GitHub: [@Schrodinger71](https://github.com/Schrodinger71)


AnagiriumBot — это кастомный Discord-бот, разработанный специально для нужды Проекта "Дельта". Он реализует уникальные команды и функции, включая управление голосовыми каналами, интеграцию с GitHub Actions и другие полезные фичи для администраторов и пользователей.

---

## 📦 Возможности

- ⚙️ **Автоматическое завершение работы**, если уже запущен GitHub workflow `Deploy Discord AnagariBot`
- 🔐 **Проверка связь с основным репозиторием через GitHub API**
- 🎙 **Управление приватными голосовыми каналами** (аналог VoiceMaster):
  - `Name`, `Limit`, `Status`, `Game`, `LSM`, `Bitrate`, `Text`, `Claim`, `Permit`, `Reject` и др.
- 💬 **Логирование сообщений** и автоматические проверки
- 🧪 Поддержка расширения функционала и кастомных команд

---

## 🚀 Быстрый старт

1. Клонируй репозиторий:
   ```bash
   git clone https://github.com/<твое_имя_пользователя>/AnagiriumBot.git
   cd AnagiriumBot


2. Установи зависимости:

   ```bash
   pip install -r requirements.txt
   ```

3. Создай файл `.env` или `config.py` и укажи свои переменные:

   * `DISCORD_TOKEN`
   * `GIT_PAT_TOKEN`
   * `AUTHOR`, `REPO` — для GitHub API

4. Запусти бота:

   ```bash
   python main.py
   ```

---

## 🔐 Переменные окружения

| Переменная      | Описание                          |
| --------------- | --------------------------------- |
| `DISCORD_TOKEN` | Токен Discord-бота                |
| `GIT_PAT_TOKEN` | GitHub Personal Access Token      |
| `AUTHOR`        | Никнейм автора репозитория GitHub |
| `REPO`          | Название репозитория              |

---

## 📁 Структура проекта

```
AnagiriumBot/
├── main.py                   # Точка входа
├── config.py / .env          # Конфигурация
├── events/
│   └── on_ready.py           # Обработка запуска
├── modules/
│   └── check_workflows.py    # GitHub workflow проверка
├── commands/                 # Пользовательские команды
│   └── voice_management.py   # Команды управления голосом
└── requirements.txt          # Зависимости
```

---
