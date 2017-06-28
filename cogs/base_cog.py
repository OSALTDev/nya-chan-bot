class BaseCog(object):
    def __init__(self, bot):
        self.bot = bot
        self.config = self.bot.config
        # TODO: add logger here.

    def auto_delete(self, func):
        async def delete(ctx):
            func(ctx)
            await ctx.channel.send('Command done')

        return delete
