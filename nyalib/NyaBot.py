import discord
from discord.ext import commands
from discord.ext.commands.bot import _is_submodule
from nyalib.config import AppConfig
from nyalib.CustomContext import CustomContext
from nyalib.HelpCommand import Command
import sys


class ThrowawayException(Exception):
    pass


class NyaBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.config = AppConfig()
        kwargs.update(command_prefix=self.config.bot.prefix, description=self.config.bot.description,
                      help_command=Command(dm_help=True))
        super().__init__(*args, **kwargs)

    def _load_from_module_spec(self, lib, key):
        try:
            if not hasattr(lib, 'Cog'):
                if not hasattr(lib, 'setup'):
                    raise discord.ClientException

                setup = lib.setup
            elif not hasattr(lib.Cog, 'setup'):
                raise discord.ClientException
            else:
                setup = lib.Cog.setup
        except discord.ClientException:
            del sys.modules[key]
            raise commands.NoEntryPointError(key)

        try:
            setup(self)
        except Exception as e:
            self._remove_module_references(lib.__name__)
            self._call_module_finalizers(lib, key)
            raise commands.ExtensionFailed(key, e) from e
        else:
            self._BotBase__extensions[key] = lib

    def _call_module_finalizers(self, lib, key):
        try:
            if hasattr(lib, "Cog"):
                func = getattr(lib.Cog, 'teardown')
            else:
                func = getattr(lib, 'teardown')
        except AttributeError:
            pass
        else:
            try:
                func(self)
            except Exception:
                pass
        finally:
            self._BotBase__extensions.pop(key, None)
            sys.modules.pop(key, None)
            name = lib.__name__
            for module in list(sys.modules.keys()):
                if _is_submodule(name, module):
                    del sys.modules[module]

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
