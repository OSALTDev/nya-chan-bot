import discord
import logging
from discord.ext import commands
from .context import CommandContext
from .config import Bot as BotConfig

if BotConfig.debug:
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='discord.debug.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

__all__ = ("BotBase", "BotConfig")


# Nya-Chan base class, inherits
class BotBase(commands.Bot):
    def __init__(self, *args, **kwargs):
        # Add or update bot token in kwargs
        kwargs.update(command_prefix=BotConfig.token)
        super().__init__(*args, **kwargs)

        # Nya-Chan logger
        self.logger = logging.getLogger('nya')

        # Different file and logging level for debugging
        if BotConfig.debug:
            self.logger.setLevel(logging.DEBUG)
            handler = logging.FileHandler(filename='nya.debug.log', encoding='utf-8', mode='w')
        else:
            self.logger.setLevel(logging.INFO)
            handler = logging.FileHandler(filename='nya.debug.log', encoding='utf-8', mode='w')

        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.logger.addHandler(handler)

    # Setting our custom context
    async def process_commands(self, message):
        if message.author.bot:
            return

        ctx = await self.get_context(message, cls=CommandContext)
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
