from bot_init import bot
from config import LOG_TECH_CHANNEL
from events.utils import send_console_style_log


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
