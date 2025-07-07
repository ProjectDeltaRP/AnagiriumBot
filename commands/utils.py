from disnake import Member, TextChannel
from disnake.ext import commands

import data
from config import (DEPARTMENT_ROLES, FULL_PERMISSION_USERS, GUILD_ID,
                    ROLE_WHITELISTS)


def has_any_role_by_keys(*whitelist_keys):
    """
    Декоратор для проверки, имеет ли пользователь одну из указанных ролей по ключам.
    Если пользователь — есть в FULL_PERMISSION_USERS, доступ разрешён всегда.
    При отказе выводятся названия нужных ролей без пинга.
    """

    async def predicate(ctx):
        if ctx.author.id in FULL_PERMISSION_USERS:
            return True

        user_role_ids = [role.id for role in ctx.author.roles]

        # Собираем все разрешённые ID ролей по ключам
        allowed_role_ids = set()
        for key in whitelist_keys:
            allowed_role_ids.update(ROLE_WHITELISTS.get(key, []))

        # Если хотя бы одна из ролей у пользователя есть — пропускаем
        if any(role_id in allowed_role_ids for role_id in user_role_ids):
            return True

        # Если команда выполнена на указанном сервере — показываем имена ролей
        if ctx.guild and ctx.guild.id == GUILD_ID:
            role_names = []
            for role_id in allowed_role_ids:
                role = ctx.guild.get_role(role_id)
                if role:
                    role_names.append(role.name)

            if role_names:
                formatted_roles = ", ".join(f"`{name}`" for name in role_names)
                await ctx.send(
                    f"❌ У вас нет доступа к этой команде.\nТребуемые роли: {formatted_roles}"
                )
            else:
                await ctx.send("❌ У вас нет доступа к этой команде. (Роли не найдены)")
        else:
            await ctx.send("❌ У вас нет доступа к этой команде.")

        return False

    return commands.check(predicate)

def get_user_private_channel(user):
    if user.voice and user.voice.channel and user.voice.channel.id in data.private_channels.values():
        if data.private_channels.get(str(user.id)) == user.voice.channel.id:
            return user.voice.channel
    return None

async def process_rank(guild, action: str, dept: str, member: Member, log_channel: TextChannel = None):
    """
    Универсальная функция для управления рангами.
    Параметры:
    - guild: объект сервера
    - action: "up", "down", "clear"
    - dept: ключ из DEPARTMENT_ROLES
    - member: участник
    - log_channel: канал для вывода результата (если None — ничего не отправлять)
    """
    cfg = DEPARTMENT_ROLES[dept]
    dept_role_ids = list(cfg["ranks"].values())
    dept_group_role = guild.get_role(cfg["group"])
    roles = [guild.get_role(rid) for rid in dept_role_ids]

    # Вспомогательная функция для обновления групповой роли
    async def update_group_role():
        has_dept_role = any(role in member.roles for role in roles)
        if has_dept_role and dept_group_role not in member.roles:
            await member.add_roles(dept_group_role, reason="Добавление групповой роли отдела")
        elif not has_dept_role and dept_group_role in member.roles:
            await member.remove_roles(dept_group_role, reason="Удаление групповой роли отдела")

    if action == "up":
        current_roles = [r for r in roles if r in member.roles]

        if not current_roles:
            new_role = guild.get_role(dept_role_ids[0])
            await member.add_roles(new_role, reason="Начальное назначение ранга отдела")
            msg = f"✅ {member.mention} назначен на роль {new_role.name}"
        else:
            current_role = max(current_roles, key=lambda r: dept_role_ids.index(r.id))
            current_index = dept_role_ids.index(current_role.id)

            if current_index + 1 >= len(dept_role_ids):
                msg = f"✅ {member.mention} уже имеет максимальный ранг {current_role.name}"
            else:
                await member.remove_roles(current_role, reason="Повышение ранга")
                new_role = guild.get_role(dept_role_ids[current_index + 1])
                await member.add_roles(new_role, reason="Повышение ранга")
                msg = f"✅ {member.mention} повышен до {new_role.name}"

    elif action == "down":
        current_roles = [r for r in roles if r in member.roles]

        if not current_roles:
            msg = f"❌ У {member.mention} нет роли из отдела `{dept}` для понижения."
        else:
            current_role = max(current_roles, key=lambda r: dept_role_ids.index(r.id))
            current_index = dept_role_ids.index(current_role.id)

            if current_index == 0:
                await member.remove_roles(current_role, reason="Удаление самой низкой роли отдела")
                msg = f"✅ {member.mention} имел минимальную роль {current_role.name}, она удалена."
            else:
                await member.remove_roles(current_role, reason="Понижение ранга")
                new_role = guild.get_role(dept_role_ids[current_index - 1])
                await member.add_roles(new_role, reason="Понижение ранга")
                msg = f"✅ {member.mention} понижен до {new_role.name}"

    else:  # clear
        await member.remove_roles(*roles, reason="Очистка рангов отдела")
        msg = f"✅ Все роли отдела `{dept}` удалены у {member.mention}"

    # Обновляем групповую роль
    await update_group_role()

    if log_channel:
        await log_channel.send(msg)

    return msg
