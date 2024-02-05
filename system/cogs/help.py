import disnake, pytz, datetime, io
from disnake.ext import commands
from typing import Optional
from assets.enums import *
from assets.database import Database
from .Collectors.buttons import Helpbuttons, Closebuttons


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()
        self.persistent_views_added = False

    async def close_ticket(self, interaction):
        await interaction.response.defer()
        user = interaction.user
        existing = await self.db.get_from_helping(user.id)
        channel_id = await self.db.get_channel_id(user.id)
        if existing is None:
            embed1 = disnake.Embed(title="Система обращений", description=f"У вас нету открытых обращений", color=Color.GRAY)
            embed1.set_thumbnail(url=interaction.author.display_avatar.url)
            await interaction.followup.send(embed=embed1)
            return
        if channel_id:
            channel = self.bot.get_channel(channel_id)
            await self.db.delete_helping(user.id)
            await channel.edit(locked=True, archived=True)
            embed = disnake.Embed(title='Диалог был прерван!', description='Вы решили прервать диалог\nЕсли Вы будете прерывать диалог без веской причины, то можете получить\nблокировку в нашей службе поддержки', color=Color.GRAY)
            await user.send(embed=embed)

    @commands.slash_command(name="помощь", description="Задать вопрос, на который интересует ответ")
    async def помощь(self, interaction, вопрос: str = commands.Param(description="Распишите ваш вопрос, далее мы свяжемся с вами")):
        await interaction.response.defer(ephemeral=True)
        role = interaction.guild.get_role(1187467271505989713)
        forum = self.bot.get_channel(DevChannels.FORUM)
        existing_ticket = await self.db.get_from_helping(interaction.user.id)
        if existing_ticket:
            embed = disnake.Embed(title="Задать вопрос по серверу", description=f"{interaction.author.mention},У вас **уже** есть **открытый** вопрос, **дождитесь** на него ответа", color=Color.GRAY)
            embed.set_thumbnail(url=interaction.author.display_avatar.url)
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
    
        embed1 = disnake.Embed(
            title="Задать вопрос по серверу", 
            description=f"{interaction.author.mention},Вы **успешно** задали вопрос, **ожидайте** ответа", 
            color=Color.GRAY
        )
        embed1.set_thumbnail(url=interaction.author.display_avatar.url)
        await interaction.followup.send(embed=embed1, ephemeral=True)

        embed4 = disnake.Embed(
            title="Новое обращение", 
            description=f"Новое обращение от {interaction.user.mention} ({interaction.user.id})\n Дата `{datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M:%S')}`\n Вопрос: {вопрос}\nЗакрыть обращение можно командой </закрыть обращение:1187902364108214327>", 
            color=Color.GRAY
        )
        embed4.set_author(name="Служба поддержки", icon_url=interaction.guild.icon.url)
        embed4.set_image(url="https://cdn.discordapp.com/attachments/992883178362642453/1029462389130792970/-1.png")
        channel = await forum.create_thread(name=f"Новое обращение от {interaction.user.name}", content=f"<@{role}>", embed=embed4)

        embed2 = disnake.Embed(
            title='Ваше обращение успешно отправлено', 
            description='Ожидайте...', 
            color=Color.GRAY
        )
        embed2.set_author(name="Служба поддержки", icon_url=interaction.guild.icon.url)
        embed3 = disnake.Embed(
            title='Пиши сообщения прямо сюда', 
            description='Спасибо за обращение в нашу службу поддержки\nСейчас постараемся решить твой вопрос, оставайся на связи', 
            color=Color.GRAY
        )
        embed3.set_author(name="Служба поддержки", icon_url=interaction.guild.icon.url)
        await interaction.user.send(embed=embed2)
        await interaction.user.send(embed=embed3, view=Helpbuttons(self))

        date = channel.message.created_at.astimezone(pytz.timezone('Europe/Moscow')).strftime("%Y-%m-%d %H:%M:%S")
        await self.db.insert_helping(interaction.user.id, channel.thread.id, date)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if isinstance(message.channel, disnake.DMChannel):
            await self.dm_msg(message)
        else:
            await self.guild_msg(message)

    async def dm_msg(self, message: disnake.Message):
        channel_id = await self.db.get_channel_id(message.author.id)
        if channel_id:
            channel = self.bot.get_channel(channel_id)
            embed = await self.create_embed(message)
            await self.send_message(channel, embed, message.attachments)

    async def guild_msg(self, message: disnake.Message):
        user_id = await self.db.get_user_id(message.channel.id)
        if user_id:
            user = self.bot.get_user(user_id)
            embed = await self.create_embed(message)
            await self.send_message(user, embed, message.attachments)

    async def create_embed(self, message: disnake.Message) -> disnake.Embed:
        embed = disnake.Embed(description=f"{message.content}")
        embed.set_author(name="Система обращений", icon_url=message.author.display_avatar.url)
        return embed

    async def send_message(self, recipient, embed: disnake.Embed, attachments: Optional[list]):
        if attachments:
            for att in attachments:
                file = await att.to_file()
                # img_bytes = io.BytesIO()
                # file.save(img_bytes)
                # img_bytes.seek(0)
                # embed.set_image(file=disnake.File(img_bytes, filename=file.filename))
                embed.set_image(url=f"attachment://{file.filename}")
                await recipient.send(embed=embed, file=file)
        else:
            await recipient.send(embed=embed)

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     if message.author.bot:
    #         return

    #     if isinstance(message.channel, disnake.DMChannel):
    #         channel_id = await self.db.get_channel_id(message.author.id)
    #         if channel_id:
    #             channel = self.bot.get_channel(channel_id)
    #             embed1 = disnake.Embed(description=f"{message.author.mention}:\n{message.content}")
    #             embed1.set_author(name="Система обращений", icon_url=message.author.display_avatar.url)
    #             if message.attachments:
    #                 for att in message.attachments:
    #                     file = await att.to_file()
    #                     embed1.set_image(url=f"attachment://{file.filename}")
    #                     await channel.send(embed=embed1, file=file)
    #             else:
    #                 # print(f"{message.author.name}: {message.content}")
    #                 await channel.send(embed=embed1)

    #     else:
    #         user_id = await self.db.get_user_id(message.channel.id)
    #         if user_id:
    #             user = self.bot.get_user(user_id)
    #             embed = disnake.Embed(description=f"{message.content}")
    #             embed.set_author(name="Служба поддержки", icon_url=message.guild.icon.url)
    #             if message.attachments:
    #                 for att in message.attachments:
    #                     file = await att.to_file()
    #                     embed.set_image(url=f"attachment://{file.filename}")
    #                     await user.send(embed=embed, file=file)
    #             else:
    #                 # print(f"{message.author.name}: {message.content}")
    #                 await user.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        if self.persistent_views_added:
            return
        
        view = disnake.ui.View()
        self.bot.add_view(view=Helpbuttons(parent=self))
        

def setup(bot):
    bot.add_cog(Help(bot))