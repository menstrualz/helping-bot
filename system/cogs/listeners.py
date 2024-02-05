import disnake, asyncio 
from disnake.ext import commands
from assets.pool import db_pool
from assets.enums import *


class Listener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_thread_create(self, forum: disnake.Thread):
        embed = disnake.Embed(description='Не забудьте закрыть обращение командой </закрыть обращение:1186785323745816748>\nесли пользователь его не закрыл и у него нет вопросов', color=Color.GRAY)
        embed.set_author(name='Система обращений', icon_url=forum.guild.icon.url)
        msg = await forum.send(embed=embed)
        await msg.pin()

    @commands.Cog.listener()
    async def on_connect(self):
        await db_pool.create_pool()
        await asyncio.sleep(1)

    @commands.Cog.listener()
    async def on_disconnect(self):
        await db_pool.close_pool()
        await asyncio.sleep(1)

    @commands.Cog.listener()
    async def on_resumed(self):
        await db_pool.create_pool()
        await asyncio.sleep(1)

def setup(bot):
    bot.add_cog(Listener(bot))