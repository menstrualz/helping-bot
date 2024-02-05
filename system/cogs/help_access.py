import disnake
from disnake.ext import commands
from .Collectors.selects import UserSelectToStaff
from assets.enums import *


class UserSelectCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.slash_command(name="добавить")
    async def добавить(self, interaction):
        pass

    @добавить.sub_command(name="стафф")
    async def стафф(self, interaction):
        view = disnake.ui.View()
        view.add_item(UserSelectToStaff())
        embed = disnake.Embed(
            description='В выпадающем меню выберите пользователя, которого хотите добавить в staff службы поддержки', 
            color=Color.GRAY
        )
        embed.set_image(url='https://cdn.discordapp.com/attachments/992883178362642453/1029462389130792970/-1.png')
        embed.set_author(name='Управление службой поддержки', icon_url=interaction.guild.icon.url)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

def setup(bot):
    bot.add_cog(UserSelectCog(bot))
