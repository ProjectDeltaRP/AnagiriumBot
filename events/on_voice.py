import random
import disnake

import data
from bot_init import bot

ENTRY_CHANNELS = {
    1374481957710467143: "СБ",
    1374484072528609330: "АС",
    1374484348123877436: "МС",
    1374484217529897106: "НС",
    # и т.д.
}

@bot.event
async def on_voice_state_update(member, before, after):
    print(f"VOICE EVENT | {member} | {before.channel} → {after.channel}")
    if before.channel == after.channel:
        return

    if after.channel and after.channel.id in ENTRY_CHANNELS:
        guild = member.guild
        category = after.channel.category

        overwrites = {
            guild.default_role: disnake.PermissionOverwrite(view_channel=False),
            member: disnake.PermissionOverwrite(view_channel=True, connect=True, manage_channels=True),
            guild.me: disnake.PermissionOverwrite(view_channel=True)
        }

        freq = f"{random.randint(60, 110)}.{random.randint(0, 9)}"
        tag = ENTRY_CHANNELS[after.channel.id]
        channel = await guild.create_voice_channel(
            name=f"Частота {tag}-{freq}: {member.display_name}",
            category=category,
            overwrites=overwrites,
            user_limit=5
        )

        data.private_channels[str(member.id)] = channel.id
        await member.move_to(channel)

        # Отправляем инструкцию в текстовый канал с таким же ID, как у голосового
        text_channel = guild.get_channel(after.channel.id)
        if text_channel is None:
            # Если текстового канала с таким ID нет,
            # можно отправить в первый доступный текстовый канал категории
            text_channel = None
            if category:
                for ch in category.channels:
                    if isinstance(ch, disnake.TextChannel):
                        text_channel = ch
                        break

        if text_channel:
            embed = disnake.Embed(
                title="🎙 Управление приватным голосовым каналом",
                description=(
                    f"Привет, {member.mention}! Это твой приватный голосовой канал.\n\n"
                    "🔹 **Как управлять каналом:**\n"
                    "• Используй права **Управление каналом**, чтобы настроить доступ.\n"
                    "• Чтобы покинуть канал — просто выйди из него.\n"
                    "• Канал удалится автоматически, когда все уйдут.\n\n"
                    "Если нужна помощь — обратись к администрации."
                ),
                color=0x2f3136,
                timestamp=disnake.utils.utcnow()
            )
            embed.set_footer(text="Автоматически созданный канал")

            await text_channel.send(embed=embed)

    # Удаление пустых приватных каналов
    if before.channel and before.channel.id in data.private_channels.values():
        if len(before.channel.members) == 0:
            print(f"Удаляю канал {before.channel.name} (ID {before.channel.id}) — пустой")
            await before.channel.delete()
            data.private_channels = {
                k: v for k, v in data.private_channels.items()
                if v != before.channel.id
            }
            print("Канал удалён, словарь обновлён")
