"""
Модуль предназначенный для общих комманд бота
"""

from bot_init import bot


@bot.command(name="ping", help="Проверяет задержку бота.")
async def ping(ctx):
    """
    Команда для проверки задержки бота.
    """
    latency = round(bot.latency * 1000)
    emoji = "🏓" if latency < 100 else "🐢"
    await ctx.send(f"{emoji} Pong! Задержка: **{latency}ms**")
