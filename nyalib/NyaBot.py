import discord
from discord.ext import commands
from discord.ext.commands.bot import _is_submodule
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
        kwargs.update(command_prefix=self.config.bot.prefix, description=self.config.bot.description,
                      pm_help=True, formatter=Formatter())
        super().__init__(*args, **kwargs)

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

    def unload_extension(self, name):
        lib = self.extensions.get(name)
        if lib is None:
            return

        lib_name = lib.__name__

        for cogname, cog in self.cogs.copy().items():
            if _is_submodule(lib_name, cog.__module__):
                self.remove_cog(cogname)

        for cmd in self.all_commands.copy().values():
            if cmd.module is not None and _is_submodule(lib_name, cmd.module):
                if isinstance(cmd, commands.GroupMixin):
                    cmd.recursively_remove_all_commands()
                self.remove_command(cmd.name)

        for event_list in self.extra_events.copy().values():
            remove = []
            for index, event in enumerate(event_list):
                if event.__module__ is not None and _is_submodule(lib_name, event.__module__):
                    remove.append(index)

            for index in reversed(remove):
                del event_list[index]

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
            del lib
            del self.extensions[name]
            del sys.modules[name]
            for module in list(sys.modules.keys()):
                if _is_submodule(lib_name, module):
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
