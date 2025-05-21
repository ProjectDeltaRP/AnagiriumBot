import data
from bot_init import bot


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
