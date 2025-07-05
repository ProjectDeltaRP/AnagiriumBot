from disnake import Member
from disnake.ext import commands

from bot_init import bot
from commands.utils import has_any_role_by_keys, process_rank
from config import DEPARTMENT_ROLES, GUILD_ID


@bot.slash_command(description="Управление рангами отдела", guild_ids=[GUILD_ID])
@has_any_role_by_keys("super_head_project", "head_project", "middle_admin")
async def rank(inter,
               action: str = commands.Param(choices=["up", "down", "clear"]),
               dept: str = commands.Param(choices=list(DEPARTMENT_ROLES.keys())),
               member: Member = None):
    """Пример: /rank up ad @user"""
    if member is None:
        return await inter.response.send_message("Укажите участника.", ephemeral=True)

    msg = await process_rank(inter.guild, action, dept, member)
    await inter.response.send_message(msg)
