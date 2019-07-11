try:
    import discord
    from discord.ext import commands

    if discord.__version__ != "1.2.3":
        raise Exception("You need to have Discord.py 1.2.3 installed")
except ModuleNotFoundError as e:
    raise Exception("Please make sure to install from the requirements.txt file")

import logging
import database
from .help import NyaHelp
from .context import CommandContext
from .config import Bot as BotConfig, Config

# Discord debug logging
if Config.debug:
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='logs/discord.debug.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

__all__ = ("BotBase", "BotConfig", "Config")


# Nya-Chan base class, inherits
class BotBase(commands.Bot):
    def __init__(self, *args, **kwargs):
        # Add or update bot token in kwargs
        def get_prefix(bot, message):
            guild = bot.get_cog("Core").db.find(id=str(message.guild.id))
            try:
                return guild["prefix"]
            except (IndexError, TypeError):
                return BotConfig.prefix

        kwargs.update(command_prefix=get_prefix, help_command=NyaHelp())
        super().__init__(*args, **kwargs)

        # Nya-Chan logger
        self.logger = logging.getLogger('nya')

        # Different file and logging level for debugging
        self.logger.setLevel(logging.DEBUG if Config.debug else logging.INFO)
        handler = logging.FileHandler(filename='logs/nya.log', encoding='utf-8', mode='w')

        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.logger.addHandler(handler)

        try:
            self.database = database.Arango()
        except database.ConnectionError as e:
            raise Exception(f"A connection to your database at {database.DBConfig.host}:{database.DBConfig.port} "
                            "could not be established") from e

    # Setting our custom context
    async def process_commands(self, message):
        if message.author.bot:
            return

        permissions_cog = self.get_cog("Permissions")
        ctx = await self.get_context(message, cls=CommandContext)

        if not ctx.command:
            return

        if await permissions_cog.execution_allowed(ctx):
            await self.invoke(ctx)

    # Print some basic information on boot
    async def on_ready(self):
        print('######################################################')
        print('#                      Nya Chan                      #')
        print('######################################################')

        print(f'Discord.py version : {discord.__version__}')
        print(f'Bot User : {self.user}')

        app_info = await self.application_info()
        self.owner_id = app_info.owner.id
        print(f'Bot Owner : {app_info.owner.id}')

        url = discord.utils.oauth_url(app_info.id)
        print(f'OAuth URL : {url}')
