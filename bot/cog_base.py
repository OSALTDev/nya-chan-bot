from discord.ext.commands import Cog


class Base(Cog):
    def __init__(self, bot):
        self.bot = bot
