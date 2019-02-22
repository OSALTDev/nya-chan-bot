from discord.ext import commands
from nyalib.config import AppConfig


class ThrowawayException(Exception):
    pass


class NyaBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.config = AppConfig()
        super().__init__(*args, command_prefix=self.config.bot.prefix, description=self.config.bot.description,
                         pm_help=True,
                         **kwargs)
