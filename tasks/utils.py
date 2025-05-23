import json
import data
from bot_init import bot
from config import BACKUP_CHANNEL_ID

DATA_MESSAGE_PREFIX = "[PRIVATE_CHANNELS_BACKUP]"

async def save_data():
    backup_channel = bot.get_channel(BACKUP_CHANNEL_ID)
    if not backup_channel:
        print("Канал бэкапа не найден!")
        return

    # Удаляем старые сообщения с бэкапом
    async for msg in backup_channel.history(limit=50):
        if msg.content.startswith(DATA_MESSAGE_PREFIX):
            try:
                await msg.delete()
            except Exception as e:
                print(f"Ошибка удаления сообщения бэкапа: {e}")

    data_to_save = {
        "private_channels": data.private_channels,
        "trigger_channels": data.trigger_channels
    }
    data_json = json.dumps(data_to_save, ensure_ascii=False)
    await backup_channel.send(f"{DATA_MESSAGE_PREFIX}```json\n{data_json}\n```")
    print("Сохранены данные о приватных и триггер-каналах.")


async def restore_data():
    try:
        backup_channel = await bot.fetch_channel(BACKUP_CHANNEL_ID)
    except Exception as e:
        print(f"Канал бэкапа не найден или ошибка получения: {e}")
        return

    async for msg in backup_channel.history(limit=50):
        if msg.content.startswith(DATA_MESSAGE_PREFIX):
            try:
                content = msg.content[len(DATA_MESSAGE_PREFIX):].strip()
                if content.startswith("```json") and content.endswith("```"):
                    content = content[7:-3].strip()
                loaded = json.loads(content)
                data.private_channels = loaded.get("private_channels", {})
                data.trigger_channels = {int(k): v for k, v in loaded.get("trigger_channels", {}).items()}
                print("Восстановлены данные:", loaded)
                return
            except Exception as e:
                print("Ошибка при восстановлении:", e)
