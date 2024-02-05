import disnake, asyncio
from disnake.ext import commands
from assets.enums import *
from assets.database import Database


class Closehelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()

    @commands.slash_command(name="закрыть", description="Закрыть обращение принудительно")
    async def закрыть(self, interaction):
        pass

    @закрыть.sub_command(name="обращение", description="Закрыть обращение принудительно")
    async def обращение(self, interaction, user_id: str = commands.Param(description="ID пользователя, чье обращение нужно закрыть")):
        await interaction.response.defer(ephemeral=True)

        userid = int(user_id)
        user = self.bot.get_user(userid)
        channel_id = await self.db.get_channel_id(userid)
        existing = await self.db.get_from_helping(userid)

        if not user:
            embed = disnake.Embed(title="Система обращений", description=f"Пользователь с таким ID не найден.", color=Color.GRAY)
            await interaction.followup.send(embed=embed)
            return

        if existing is None:
            embed1 = disnake.Embed(title="Система обращений", description=f"У пользователя нету открытых обращений", color=Color.GRAY)
            await interaction.followup.send(embed=embed1)
            return

        if channel_id:
            channel = self.bot.get_channel(channel_id)
            if channel is None:
                embed2 = disnake.Embed(title="Система обращений", description=f"Не был найден канал обращения", color=Color.GRAY)
                await interaction.followup.send(embed=embed2)
                return

            tag = channel.parent.get_tag_by_name("Обращение Закрыто")
            await channel.add_tags(tag)
            await channel.edit(locked=True, archived=True)
            embed2 = disnake.Embed(title="Система обращений", description=f"Обращение от {user.mention} было закрыто", color=Color.GRAY)
            await interaction.followup.send(embed=embed2)

            await self.db.delete_helping(user.id)
            embed = disnake.Embed(title='Диалог был прерван!', description=f'Саппорт не получил от Вас никакого ответа, если Вы будете продолжать\nигнорировать саппортов при отправке тикета, то можете получить блокировку\nв нашей службе поддержки', color=Color.GRAY)
            await user.send(embed=embed)
        else:
            embed2 = disnake.Embed(title="Система обращений", description=f"Не был найден канал обращения", color=Color.GRAY)
            await interaction.followup.send(embed=embed2)


def setup(bot):
    bot.add_cog(Closehelp(bot))