import disnake 
from assets.enums import *
from typing import Optional

class Closebuttons(disnake.ui.View):
    def __init__(self, parent):
        super().__init__(timeout=None)
        self.parent = parent

    @disnake.ui.button(emoji="✅", style=disnake.ButtonStyle.secondary, custom_id="close_accept")
    async def close_accept_callback(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self.parent.close_ticket(interaction)
        button.disabled = True
        await interaction.edit_original_message(view=self)

    @disnake.ui.button(emoji="❌", style=disnake.ButtonStyle.secondary, custom_id="close_deny")
    async def close_deny_callback(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await interaction.response.defer()
        button.disabled = True
        await interaction.edit_original_message(view=self)

class Helpbuttons(disnake.ui.View):
    def __init__(self, parent):
        super().__init__(timeout=None)
        self.parent = parent

    @disnake.ui.button(label="Прервать диалог", style=disnake.ButtonStyle.primary, custom_id="close_1")
    async def close_1_callback(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        # await self.parent.close_ticket(interaction)
        await interaction.response.send_message(f"{interaction.author.mention}, Вы **уверены**, что хотите **прервать** диалог? Если\nВы будете прерывать диалог **без веской причины**, то **можете**\n**получить блокировку** в нашей службе поддержки\nДля **согласия** нажмите на :white_check_mark:, для отказа на :x:", view=Closebuttons(self.parent))