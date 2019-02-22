from discord.ext import commands
import discord

from cogs.base_cog import BaseCog


class Welcome(BaseCog):
    """Welcomes new members to the server via private message"""

    def __init__(self, bot):
        super().__init__(bot)

    def get_message(self, member):
        with self.cursor_context(connection_yield=True) as (cursor, connection):
            cursor.execute("""SELECT message FROM welcomes WHERE id_server = %s""", member.guild.id)
            row = cursor.fetchone()
            if not row:
                cursor.execute("""INSERT INTO welcomes (id, id_server, message) VALUES (null, %s, "")""",
                               member.guild.id)
                text = ""
                connection.commit()
            else:
                text = row[0]

        return text.format(member, member.guild)

    async def member_join(self, member):
        user_role = discord.utils.get(member.guild.roles, name="Users")
        if user_role is not None:
            await member.add_roles(user_role, reason="Safeguard against pruning.")
        text = self.get_message(member)
        try:
            await member.send(text)
        except:
            pass

    @commands.command(description='Send the welcome message via private message again.')
    @commands.guild_only()
    async def welcome(self, ctx):
        """Resend welcome message"""
        text = self.get_message(ctx.author)
        try:
            await ctx.author.send(text)
        except:
            pass


def setup(bot):
    cog = Welcome(bot)
    bot.add_listener(cog.member_join, "on_member_join")
    bot.add_cog(cog)
