import json

import data
from bot_init import bot
from config import BACKUP_CHANNEL_ID

DATA_MESSAGE_PREFIX = "[PRIVATE_CHANNELS_BACKUP]"


async def save_private_channels():
    backup_channel = bot.get_channel(BACKUP_CHANNEL_ID)
    if not backup_channel:
        print("Канал логов не найден!")
        return

    # Удаляем старые сообщения с бэкапом
    async for msg in backup_channel.history(limit=50):
        if msg.content.startswith(DATA_MESSAGE_PREFIX):
            await msg.delete()

    data_json = json.dumps(data.private_channels)
    await backup_channel.send(f"{DATA_MESSAGE_PREFIX}```json\n{data_json}\n```")
    print("Сохранены данные о приватных каналах.")



async def restore_private_channels():
    backup_channel = bot.get_channel(BACKUP_CHANNEL_ID)
    if not backup_channel:
        print("Канал логов не найден!")
        return

    async for msg in backup_channel.history(limit=50):
        if msg.content.startswith(DATA_MESSAGE_PREFIX):
            try:
                content = msg.content.removeprefix(DATA_MESSAGE_PREFIX).strip("```json\n").strip("```")
                data.private_channels = json.loads(content)
                print("Восстановлены данные:", data.private_channels)
                return
            except Exception as e:
                print("Ошибка при восстановлении:", e)
