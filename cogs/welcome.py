from discord.ext import commands

from cogs.base_cog import BaseCog


class Welcome(BaseCog):
    """Welcomes new members to the server via private message"""

    def __init__(self, bot):
        super().__init__(bot)

    def get_message(self, member):
        guild = member.guild
        connection = self.config.db_connection()
        cursor = connection.cursor()
        cursor.execute("""SELECT message FROM welcomes WHERE id_server = %s""", guild.id)
        rows = cursor.fetchall()
        if len(rows) == 0:
            cursor.execute("""INSERT INTO welcomes (id, id_server, message) VALUES (null, %s, "")""", guild.id)
            connection.commit()
            text = ""
        else:
            text = rows[0][0]
        connection.close()
        return text.format(member, guild)

    async def member_join(self, member):
        user_role = None
        for role in member.guild.roles:
            if role.name == "User":
                user_role = role
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
        member = ctx.message.author
        text = self.get_message(member)
        try:
            await member.send(text)
        except:
            pass


def setup(bot):
    cog = Welcome(bot)
    bot.add_listener(cog.member_join, "on_member_join")
    bot.add_cog(cog)
