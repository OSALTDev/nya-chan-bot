from discord.ext import commands

from cogs.base_cog import BaseCog
from nyalib.small_helpers import filterTextForSqlInjection


class Customs(BaseCog):
    """Welcomes new members to the server via private message"""

    def __init__(self, bot):
        super().__init__(bot)

    @commands.command(description='Sends a custom message.')
    @commands.guild_only()
    async def cc(self, ctx, command_name: str):
        """Sends a custom message"""
        command_name = filterTextForSqlInjection(command_name)  # as the command name is taken directly from user input
        guild = ctx.guild
        connection = self.config.db_connection()
        cursor = connection.cursor()
        cursor.execute("""SELECT `message` FROM `custom_commands` WHERE `id_server` = %s AND `command` = %s""",
                       (guild.id, command_name))
        rows = cursor.fetchall()
        connection.close()
        if len(rows) == 0:
            await ctx.channel.send(
                'The custom message **{}** doesn\'t exist, {}'.format(command_name, ctx.author.mention))
            return False
        text = rows[0][0]
        await ctx.channel.send(text)


def setup(bot):
    cog = Customs(bot)
    bot.add_cog(cog)
