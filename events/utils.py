from datetime import datetime

from disnake import TextChannel

from bot_init import bot


async def send_console_style_log(channel: TextChannel):
    """Отправляет стилизованное сообщение о запуске в лог-канал"""
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    ascii_art = f"""
```diff
+-----------------------------------------------------+
| SCPINET BOTT {current_time}                       |
|                                                     |
-->> SYSTEM BOOT SEQUENCE INITIATED                   |
-->> BOT CORE ONLINE                                  |
|                                                     |
{await get_guild_status()}           |
|                                                     |
-->> ALL SYSTEMS NOMINAL                              |
-->> AWAITING USER COMMANDS                           |
+-----------------------------------------------------+
```
"""
    await channel.send(ascii_art)


async def get_guild_status() -> str:
    """Форматирует информацию о серверах"""
    guilds = bot.guilds
    status = []
    for i, guild in enumerate(guilds[:3], 1):
        status.append(f"|  {i}. {guild.name:<25} [{len(guild.members):>3} users]")

    if len(guilds) > 3:
        status.append(f"|  ...and {len(guilds)-3} more servers")

    return '\n'.join(status)
