from bot_init import bot, sheet_manager

from disnake.ext import commands
from disnake import Embed, ui, ButtonStyle

RANGE_NAME = "Игроки (включая администрацию)!A1:H"

class PlayersView(ui.View):
    def __init__(self, data, per_page=5):
        super().__init__(timeout=None)
        self.data = data
        self.per_page = per_page
        self.page = 0
        self.max_page = (len(data) - 1) // per_page

    def get_page_embed(self):
        embed = Embed(title="Игроки (Discord ID и Роблокс профиль)")
        start = self.page * self.per_page
        end = start + self.per_page
        page_data = self.data[start:end]

        for row in page_data:
            discord_id = row.get('Дискорд ID', 'Нет данных')
            roblox_profile = row.get('Роблокс профиль', 'Нет данных')
            joined_date = row.get('Дата присоединения', 'Нет данных')
            ac = 'АС' if row.get('АС', '').strip() == '+' else ''
            ns = 'НС' if row.get('НС', '').strip() == '+' else ''
            sb = 'СБ' if row.get('СБ', '').strip() == '+' else ''
            ms = 'МС' if row.get('МС', '').strip() == '+' else ''
            departments = ', '.join(filter(None, [ac, ns, sb, ms]))
            if not departments:
                departments = "Нет отделов"

            embed.add_field(
                name=f"Discord ID: {discord_id}",
                value=(
                    f"Роблокс профиль: {roblox_profile}\n"
                    f"Дата присоединения: {joined_date}\n"
                    f"Отделы: {departments}"
                ),
                inline=False
            )

        embed.set_footer(text=f"Страница {self.page + 1} из {self.max_page + 1}")
        return embed

    @ui.button(label="◀", style=ButtonStyle.secondary)
    async def prev_page(self, button, inter):
        if self.page > 0:
            self.page -= 1
            await inter.response.edit_message(embed=self.get_page_embed(), view=self)
        else:
            await inter.response.defer()

    @ui.button(label="▶", style=ButtonStyle.secondary)
    async def next_page(self, button, inter):
        if self.page < self.max_page:
            self.page += 1
            await inter.response.edit_message(embed=self.get_page_embed(), view=self)
        else:
            await inter.response.defer()

@bot.slash_command(description="Показать таблицу Игроки (Discord ID и Роблокс профиль)")
async def players(inter):
    data = sheet_manager.get_dicts(RANGE_NAME)
    if not data:
        await inter.response.send_message("Таблица пуста или данные не найдены.")
        return

    view = PlayersView(data)
    embed = view.get_page_embed()
    await inter.response.send_message(embed=embed, view=view)

@bot.slash_command(description="Получить Roblox профиль по Discord ID")
async def roblox(inter, discord_id: str):
    profile = sheet_manager.get_roblox_profile_by_discord_id(discord_id, RANGE_NAME)
    if profile:
        await inter.response.send_message(f"Roblox профиль для Discord ID `{discord_id}`: `{profile}`")
    else:
        await inter.response.send_message(f"Профиль Roblox для Discord ID `{discord_id}` не найден.")

@bot.slash_command(description="Получить Discord ID по Roblox профилю")
async def discordid(inter, roblox_profile: str):
    discord_id = sheet_manager.get_discord_id_by_roblox_profile(roblox_profile, RANGE_NAME)
    if discord_id:
        await inter.response.send_message(f"Discord ID для Roblox профиля `{roblox_profile}`: `{discord_id}`")
    else:
        await inter.response.send_message(f"Discord ID для Roblox профиля `{roblox_profile}` не найден.")
