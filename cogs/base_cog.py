from discord.ext import commands
import contextlib


class BaseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = self.bot.config
        # TODO: add logger here.

    @contextlib.contextmanager
    def cursor_context(self, commit=False):
        connection = self.config.db_connection()
        cursor = connection.cursor()
        yield cursor
        if commit:
            connection.commit()
        connection.close()

    async def no_invoke_help(self, ctx):
        await ctx.invoke(self.bot.get_command("help"), *ctx.command.qualified_name.split())

    @classmethod
    def setup(cls, bot):
        # default setup method
        bot.add_cog(cls(bot))
