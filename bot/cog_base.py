from bot import BotBase
from discord.ext import commands


class Base(commands.Cog):
    def __init__(self, bot: BotBase):
        self.bot = bot
        self.bot.add_cog(self)
