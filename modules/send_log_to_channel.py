import traceback

from disnake import Client, Embed, TextChannel
from disnake.abc import User

from config import LOG_TECH_CHANNEL


async def log_to_channel(bot: Client, message: str, *,
                         title: str = "Лог",
                         color: int = 0x2f3136,
                         mention: User | None = None,
                         codeblock: bool = True,
                         embed: bool = True):
    """
    Универсальная функция логирования в Discord-канал.

    :param bot: Экземпляр бота.
    :param message: Основное сообщение (текст лога).
    :param title: Заголовок эмбеда (если включен).
    :param color: Цвет эмбеда.
    :param mention: Упоминание пользователя (если нужно).
    :param codeblock: Обернуть текст в ```, если embed=False.
    :param embed: Использовать embed (по умолчанию True).
    """
    try:
        channel = bot.get_channel(LOG_TECH_CHANNEL)
        if not isinstance(channel, TextChannel):
            print("⚠️ LOG_TECH_CHANNEL не найден или не является текстовым каналом")
            return

        mention_text = f"{mention.mention} " if mention else ""

        if embed:
            emb = Embed(title=title, description=message, color=color)
            emb.set_footer(text="Логирование")
            await channel.send(content=mention_text or None, embed=emb)
        else:
            if codeblock:
                message = f"```{message}```"
            await channel.send(content=mention_text + message)

        print(f"📨 Log sent: {title}")
    except Exception:
        print("❌ Ошибка при логировании в канал:")
        traceback.print_exc()
