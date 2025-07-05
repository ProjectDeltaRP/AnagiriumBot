import asyncio

import disnake
from disnake.ext import commands

from bot_init import bot
from commands.utils import has_any_role_by_keys
from config import API_KEY_ROBLOX, GROUP_CHOICES, GROUP_COLORS
from modules.api_roblox_man import RobloxGroupManager

ITEMS_PER_PAGE = 10


class MemberPaginator(disnake.ui.View):
    def __init__(self, group_id, members):
        super().__init__(timeout=120)
        self.group_id = group_id
        self.members = members
        self.current_page = 0
        self.max_page = (len(members) - 1) // ITEMS_PER_PAGE

    def get_embed(self):
        start = self.current_page * ITEMS_PER_PAGE
        end = start + ITEMS_PER_PAGE
        page_members = self.members[start:end]

        embed = disnake.Embed(
            title=f"Участники группы: {GROUP_CHOICES.get(self.group_id, 'Неизвестная группа')}",
            description=f"ID группы: {self.group_id}\nПоказаны участники {start + 1} - {min(end, len(self.members))} из {len(self.members)}",
            color=disnake.Color.blurple()
        )

        for m in page_members:
            embed.add_field(
                name=f"{m['username']} (ID: {m['user_id']})",
                value=f"Роль: {m['role_name']} (ID роли: {m['role_id']})",
                inline=False
            )

        embed.set_footer(text=f"Страница {self.current_page + 1} из {self.max_page + 1}")
        return embed
    
    def get_embed(self):
        start = self.current_page * ITEMS_PER_PAGE
        end = start + ITEMS_PER_PAGE
        page_members = self.members[start:end]

        color = GROUP_COLORS.get(self.group_id, disnake.Color.blurple())

        embed = disnake.Embed(
            title=f"Участники группы: {GROUP_CHOICES.get(self.group_id, 'Неизвестная группа')}",
            description=f"ID группы: {self.group_id}\nПоказаны участники {start + 1} - {min(end, len(self.members))} из {len(self.members)}",
            color=color
        )

        for m in page_members:
            embed.add_field(
                name=f"{m['username']} (ID: {m['user_id']})",
                value=f"Роль: {m['role_name']} (ID роли: {m['role_id']})",
                inline=False
            )

        embed.set_footer(text=f"Страница {self.current_page + 1} из {self.max_page + 1}")
        return embed

    @disnake.ui.button(label="⬅️ Назад", style=disnake.ButtonStyle.secondary)
    async def back(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if self.current_page > 0:
            self.current_page -= 1
            await inter.response.edit_message(embed=self.get_embed(), view=self)
        else:
            await inter.response.defer()

    @disnake.ui.button(label="Вперед ➡️", style=disnake.ButtonStyle.secondary)
    async def forward(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if self.current_page < self.max_page:
            self.current_page += 1
            await inter.response.edit_message(embed=self.get_embed(), view=self)
        else:
            await inter.response.defer()

@bot.slash_command(description="Показать участников выбранной группы Roblox")
async def list_members(
    inter,
    group_id: int = commands.Param(
        description="Выберите группу",
        choices=[
            disnake.OptionChoice(name="Административная служба", value=36048024),
            disnake.OptionChoice(name="Научная служба", value=36048147),
            disnake.OptionChoice(name="Служба безопасности", value=36046821),
            disnake.OptionChoice(name="Медицинская служба", value=36048117),
        ]
    )
):
    await inter.response.defer()
    mgr = RobloxGroupManager(API_KEY_ROBLOX, [group_id])
    try:
        all_members = await asyncio.to_thread(mgr.get_members_list)
    except Exception as e:
        await inter.followup.send(f"Ошибка при получении списка: {e}")
        return

    members = all_members.get(group_id)
    if not members:
        await inter.followup.send(f"В группе {group_id} нет участников или группа не найдена.")
        return

    paginator = MemberPaginator(group_id, members)
    embed = paginator.get_embed()
    await inter.followup.send(embed=embed, view=paginator)


@bot.slash_command(description="Показать роли выбранной группы Roblox")
async def list_roles(
    inter,
    group_id: int = commands.Param(
        description="Выберите группу",
        choices=[
            disnake.OptionChoice(name="Административная служба", value=36048024),
            disnake.OptionChoice(name="Научная служба", value=36048147),
            disnake.OptionChoice(name="Служба безопасности", value=36046821),
            disnake.OptionChoice(name="Медицинская служба", value=36048117),
        ]
    )
):
    await inter.response.defer()
    try:
        mgr = RobloxGroupManager(API_KEY_ROBLOX, [group_id])
        roles = await asyncio.to_thread(mgr.get_roles, group_id)
    except Exception as e:
        await inter.followup.send(f"Ошибка при получении списка ролей: {e}")
        return

    if not roles:
        await inter.followup.send(f"В группе {group_id} нет ролей или группа не найдена.")
        return

    embed = disnake.Embed(
        title=f"Роли группы: {GROUP_CHOICES.get(group_id, 'Неизвестная группа')}",
        description=f"ID группы: {group_id}\nВсего ролей: {len(roles)}",
        color=GROUP_COLORS.get(group_id, disnake.Color.green())
    )

    for role_id, role_name in roles.items():
        embed.add_field(
            name=role_name,
            value=f"ID роли: {role_id}",
            inline=False
        )

    await inter.followup.send(embed=embed)


@bot.slash_command()
@has_any_role_by_keys("super_head_project")
async def rank_member(inter, group_id: int, user_id: int, new_role: str):
    mgr = RobloxGroupManager(API_KEY_ROBLOX, [group_id])
    try:
        mgr.change_member_role(group_id, user_id, new_role)
    except ValueError as e:
        await inter.response.send_message(f"❌ {e}")
    else:
        await inter.response.send_message(f"✅ Роль для {user_id} в группе {group_id} изменена на {new_role}")
