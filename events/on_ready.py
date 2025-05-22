from bot_init import bot
from config import LOG_TECH_CHANNEL
from events.utils import send_console_style_log
from tasks.shutdown_timer import shutdown_timer
from tasks.utils import restore_private_channels


async def start_task_if_not_running(task, task_name: str):
    """
    Запускает задачу, если она еще не запущена.
    """
    if not task.is_running():
        task.start()
        print(f"✅ Задача {task_name} запущена.")
    else:
        print(f"⚙️ Задача {task_name} уже работает.")


@bot.event
async def on_ready():
    """
    Событие, которое выполняется при запуске бота.
    """
    guild_names = [guild.name for guild in bot.guilds]
    print("✅ Connected to Discord successfully.")
    print(
        f"✅ Guilds: {guild_names}"
    )  # Выводит список серверов, к которым подключен бот.
    print(f"✅ Bot {bot.user.name} (ID: {bot.user.id}) is ready to work!")


    # Запуск восстановления данных
    await restore_private_channels()


    # Логирование запуска бота в канал
    log_channel = bot.get_channel(LOG_TECH_CHANNEL)
    if not log_channel:
        print("Channel LOG_TECH_CHANNEL not found!!")
        return
    try:
        await send_console_style_log(log_channel)
        print("✅ Startup log sent to Discord channel")
    except Exception as e:
        print(f"❌ Failed to send log: {e}")


    # Запуск всех фоновых задач
    # tasks_to_start = [
    #     (fetch_merged_pull_requests, "fetch merged pr"),

    # ]
    
    # Для дебага
    # tasks_to_start = []

    # for task, name in tasks_to_start:
    #     await start_task_if_not_running(task, name)


    # Запускаем таймер отключения через 6 часов
    shutdown_timer.start()
