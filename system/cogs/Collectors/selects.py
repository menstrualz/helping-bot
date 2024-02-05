import disnake, pytz
from datetime import datetime
from disnake.ext import commands
from assets.database import Database
from assets.enums import *


class UserSelectToStaff(disnake.ui.UserSelect):
    def __init__(self):
        self.db = Database()

        super().__init__(placeholder='Добавить в стафф', min_values=1, max_values=1)

    async def callback(self, interaction: disnake.MessageInteraction):
        await interaction.response.defer(ephemeral=True)
        member = self.values[0]
        in_staff = await self.db.get_in_staff(member.id)
        if in_staff:
            embed = disnake.Embed(
                description=f'Пользователь {member.mention} уже является частью службы поддержки', 
                color=Color.RED
            )
            embed.set_image(url='https://cdn.discordapp.com/attachments/992883178362642453/1029462389130792970/-1.png')
            embed.set_author(name='Управление службой поддержки', icon_url=interaction.guild.icon.url)
            await interaction.followup.send(embed=embed, ephemeral=True)
            return

        date = datetime.now(pytz.timezone('Europe/Moscow')).strftime("%Y-%m-%d %H:%M:%S")
        await self.db.add_staff(member.id, interaction.author.id, 0, date)