class BaseCog(object):
    def __init__(self, bot):
        self.bot = bot
        self.config = self.bot.config
        # TODO: add logger here.
