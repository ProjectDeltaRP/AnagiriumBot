from bot_init import bot


@bot.event
async def on_ready():
    """
    Событие, которое выполняется при запуске бота.
    """
    guild_names = [guild.name for guild in bot.guilds]
    print("✅ Connected to Discord successfully.")
    print(f"✅ Guilds: {guild_names}")  # Выводит список серверов, к которым подключен бот.
    print(f"✅ Bot {bot.user.name} (ID: {bot.user.id}) is ready to work!")
