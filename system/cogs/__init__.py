from .bot_status import BotStatus
from .close_help import Closehelp
from .help_access import UserSelectCog
from .listeners import Listener
from .help import Help


cogs = (
    BotStatus,
    Closehelp,
    UserSelectCog,
    Listener,
    Help
)

def setup(bot):
    for cog in cogs:
        bot.add_cog(cog(bot)) 
        for command in cog.get_application_commands(self=cog):
            print(f"загружена команда /{command.name}")