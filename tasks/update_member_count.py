import disnake
from disnake.ext import tasks

from bot_init import bot
from config import ALL_MEMBER_CHANNEL, GUILD_ID, ONLINE_MEMBER_CHANNEL


@tasks.loop(minutes=5)
async def update_member_count():
    try:
        # Получаем гильдию (сервер)
        guild = bot.get_guild(GUILD_ID)
        
        if guild is None:
            print("Guild not found")
            return

        # Получаем количество участников онлайн
        online_members = sum(1 for member in guild.members 
                            if member.status != disnake.Status.offline and not member.bot)
        
        # Получаем общее количество участников
        total_members = sum(1 for member in guild.members if not member.bot)

        # Форматируем числа (2.90K вместо 2900)
        def format_number(num):
            if num >= 1000:
                return f"{num/1000:.2f}K".replace(".00", "").replace(".", ",")
            return str(num)

        formatted_online = format_number(online_members)
        formatted_total = format_number(total_members)

        # Получаем каналы
        online_channel = guild.get_channel(ONLINE_MEMBER_CHANNEL)
        total_channel = guild.get_channel(ALL_MEMBER_CHANNEL)

        # Обновляем названия каналов
        if online_channel and isinstance(online_channel, disnake.VoiceChannel):
            await online_channel.edit(name=f"Online Members: {formatted_online}")
        
        if total_channel and isinstance(total_channel, disnake.VoiceChannel):
            await total_channel.edit(name=f"All humans: {formatted_total}")

    except Exception as e:
        print(f"Error updating member count: {e}")
