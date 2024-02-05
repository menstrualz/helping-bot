import disnake
import os
from system import cogs
from dotenv import load_dotenv
from disnake.ext import commands
from loguru import logger

bot = commands.Bot(command_prefix = "!", intents = disnake.Intents.all(), help_command = None, reload = True)

@bot.event
async def on_ready():
    logger.success(f"-> <DISCORD API  CONNECTED > {bot.user.name} запущен")

@bot.event
async def on_resumed():
    logger.warning(f"-> < DISCORD API RESUMED > {bot.user}")

@bot.event
async def on_disconnect():
    logger.critical(f"-> < DISCORD API DISCONNECTED > {bot.user}")

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

cogs.setup(bot)
bot.run(BOT_TOKEN)
