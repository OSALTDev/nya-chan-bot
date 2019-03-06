import discord
from discord.ext import commands
from nyalib.config import AppConfig
from nyalib.CustomContext import CustomContext
from nyalib.HelpFormatter import Formatter
import importlib
import sys


class ThrowawayException(Exception):
    pass


class NyaBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.config = AppConfig()
        super().__init__(*args, command_prefix=self.config.bot.prefix, description=self.config.bot.description,
                         pm_help=True, formatter=Formatter(),
                         **kwargs)

    def load_extension(self, name):
        if name in self.extensions:
            return

        lib = importlib.import_module(name)
        if not hasattr(lib, 'Cog'):
            if not hasattr(lib, 'setup'):
                del lib
                del sys.modules[name]
                raise discord.ClientException('extension ' + name + ' has neither a Cog class nor a setup function')

            lib.setup(self)
        elif not hasattr(lib.Cog, 'setup'):
            del lib
            del sys.modules[name]
            raise discord.ClientException('extension ' + name + '\'s Cog class does not have a setup function')
        else:
            lib.Cog.setup(self)

        self.extensions[name] = lib

    async def process_commands(self, message):
        if message.author.bot:
            return

        ctx = await self.get_context(message, cls=CustomContext)
        await self.invoke(ctx)

    async def on_ready(self):
        print('######################################################')
        print('#                      Nya Chan                      #')
        print('######################################################')
        print('Discord.py version : ' + discord.__version__)
        print('Bot User : ' + str(self.user))
        app_infos = await self.application_info()
        self.owner_id = app_infos.owner.id
        print('Bot Owner : ' + str(self.owner_id))
        url = discord.utils.oauth_url(app_infos.id)
        print('Oauth URL : ' + url)
