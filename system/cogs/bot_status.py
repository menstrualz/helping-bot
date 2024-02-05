import disnake, asyncio
from disnake.ext import commands
from assets.enums import *


class BotStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='статус', description='Изменить статус бота')
    @commands.is_owner()
    async def set_status(self, interaction, status=commands.Param(choices=["Онлайн", "Неактивен", "Не беспокоить", "Оффлайн"])):
        embed = disnake.Embed(title='Служба поддержки', description=f'Вы успешно сменили статус на {status}', color=Color.GRAY)
        embed.set_thumbnail(url=interaction.author.display_avatar.url)
        if status == "Онлайн":
            await self.bot.change_presence(status=disnake.Status.online)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif status == "Неактивен":
            await self.bot.change_presence(status=disnake.Status.idle)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif status == "Не беспокоить":
            await self.bot.change_presence(status=disnake.Status.dnd)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif status == "Оффлайн":
            await self.bot.change_presence(status=disnake.Status.offline)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message("Неверный статус. Возможные статусы: Онлайн, Неактивен, Не беспокоить, Оффлайн")


def setup(bot):
    bot.add_cog(BotStatus(bot))