from disnake import VoiceChannel

import data
from bot_init import bot
from commands.utils import has_any_role_by_keys
from modules.utils_data import save_data


@bot.slash_command(name="lock", description="Закрыть канал для других")
async def lock_channel(ctx):
    if ctx.author.voice and ctx.author.voice.channel.id in data.private_channels.values():
        channel = ctx.author.voice.channel
        await channel.set_permissions(ctx.guild.default_role, connect=False)
        await ctx.send("🔒 Канал заблокирован!", ephemeral=True)
    else:
        await ctx.send("Вы не в своем приватном канале!", ephemeral=True)

@bot.slash_command(name="unlock", description="Открыть канал для других")
async def unlock_channel(ctx):
    if ctx.author.voice and ctx.author.voice.channel.id in data.private_channels.values():
        channel = ctx.author.voice.channel
        await channel.set_permissions(ctx.guild.default_role, connect=True)
        await ctx.send("🔓 Канал разблокирован!", ephemeral=True)
    else:
        await ctx.send("Вы не в своем приватном канале!", ephemeral=True)

# Слэш-команда для добавления триггер-канала
@bot.slash_command(description="Добавить триггер-канал для создания приватных каналов")
@has_any_role_by_keys("head_project")
async def add_trigger_channel(inter, channel: VoiceChannel, tag: str):
    data.trigger_channels[channel.id] = tag
    await save_data()
    await inter.response.send_message(f"Добавлен триггер-канал {channel.mention} с тегом '{tag}'")


# Слэш-команда для удаления триггер-канала
@bot.slash_command(description="Удалить триггер-канал")

async def remove_trigger_channel(inter, channel: VoiceChannel):
    if channel.id in data.trigger_channels:
        del data.trigger_channels[channel.id]
        await save_data()
        await inter.response.send_message(f"Удалён триггер-канал {channel.mention}")
    else:
        await inter.response.send_message(f"Канал {channel.mention} не является триггер-каналом")


# Можно командой вывести список триггер-каналов
@bot.slash_command(description="Показать список триггер-каналов")
async def list_trigger_channels(inter):
    if not data.trigger_channels:
        await inter.response.send_message("Триггер-каналы не настроены.")
        return
    msg = "Триггер-каналы:\n"
    for ch_id, tag in data.trigger_channels.items():
        msg += f"- <#{ch_id}> с тегом '{tag}'\n"
    await inter.response.send_message(msg)
