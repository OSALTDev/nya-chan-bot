from discord.ext import commands
from nyalib.config import AppConfig


class NyaBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.config = AppConfig()
        self.loaded_cogs = []
        super().__init__(*args, command_prefix=self.config.bot.prefix, description=self.config.bot.description,
                         pm_help=True,
                         **kwargs)

    def load_cog(self, cog: str):
        try:
            self.load_extension('cogs.' + cog)
        except (AttributeError, ImportError) as e:
            print("Failed to load cog: {} due to {}".format(cog, str(e)))
            return False
        self.loaded_cogs.append(cog)

    def unload_cog(self, cog: str):
        try:
            self.unload_extension('cogs.' + cog)
        except (AttributeError, ImportError) as e:
            print("Failed to unload cog: {} due to {}".format(cog, str(e)))
            return False
        self.loaded_cogs.remove(cog)

    def reload_cog(self, cog: str):
        try:
            self.load_extension('cogs.' + cog)
            self.unload_extension('cogs.' + cog)
        except (AttributeError, ImportError) as e:
            print("Failed to unload cog: {} due to {}".format(cog, str(e)))
            return False
