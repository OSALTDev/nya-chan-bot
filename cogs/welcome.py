from discord.ext import commands
import discord

from cogs.base_cog import BaseCog


class Welcome(BaseCog, name="Welcome"):
    """Welcomes new members to the server via private message"""
    def get_message(self, guild):
        with self.cursor_context() as cursor:
            res = cursor.execute("""SELECT message FROM welcomes WHERE id_server = %s""", guild.id)
            if not res:
                cursor.execute("""INSERT INTO welcomes (id, id_server, message) VALUES (null, %s, "")""",
                               guild.id)
                return None
            else:
                row = cursor.fetchone()
                text = row[0]

        return text

    @commands.Cog.listener()
    async def on_member_join(self, member):
        user_role = discord.utils.get(member.guild.roles, name="Users")
        if user_role is not None:
            await member.add_roles(user_role, reason="Safeguard against pruning.")
        text = self.get_message(member.guild)
        if text:
            try:
                await member.send(text.format(member, member.guild))
            except discord.Forbidden:
                pass

    @commands.command(description='Send the welcome message via private message again.')
    @commands.guild_only()
    async def welcome(self, ctx):
        """Resend welcome message"""
        text = self.get_message(ctx.guild)
        if text:
            try:
                await ctx.author.send(text.format(ctx.author, ctx.guild))
            except discord.Forbidden:
                pass


def setup(bot):
    cog = Welcome(bot)
    bot.add_cog(cog)
