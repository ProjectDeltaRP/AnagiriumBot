import asyncio

from disnake.ext import tasks

from bot_init import bot
from config import SHUTDOWN_TIMER
from tasks.utils import save_private_channels


@tasks.loop(count=1)
async def shutdown_timer():
    await asyncio.sleep(SHUTDOWN_TIMER)
    await save_private_channels()
    await bot.close()
