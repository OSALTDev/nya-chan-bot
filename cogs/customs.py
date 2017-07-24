from discord.ext import commands
from cogs.base_cog import BaseCog
import discord


class Customs(BaseCog):
    """Welcomes new members to the server via private message"""

    def __init__(self, bot):
        super().__init__(bot)

    @commands.command(description='Sends a custom message.')
    @commands.guild_only()
    async def cc(self, ctx, command_name: str):
        """Sends a custom message"""
        bot_channel = self.bot.get_channel(332644650462478336)
        if bot_channel is None:
            await ctx.channel.send('The dedicated bot commands channel cannot be found')
            return False
        guild = ctx.guild
        connection = self.config.db_connection()
        cursor = connection.cursor()
        cursor.execute("""SELECT `message` FROM `custom_commands` WHERE `id_server` = %s AND `command` = %s""",
                       (guild.id, command_name))
        rows = cursor.fetchall()
        connection.close()
        if len(rows) == 0:
            await bot_channel.send(
                'The custom message **{}** doesn\'t exist, {}'.format(command_name, ctx.author.mention))
            return False
        text = rows[0][0]
        await ctx.channel.send(text)

    @commands.command(description='Explain the kicks.')
    @commands.guild_only()
    async def accident(self, ctx):
        """Explain the kicks"""
        embed = discord.Embed(title="Announcement Regarding Accidental Kicking",
                              url='https://www.youtube.com/watch?v=I9GcnRAdY2M')
        embed.add_field(name="Joker here, with an announcement for all my lovely adoring fans here at Joker Asylum!",
                        value="", inline=True)
        embed.add_field(
            name="You may have noticed we had some regulars having to rejoin this server, having been kicked!",
            value="", inline=True)
        embed.add_field(
            name="I just gotta say, ya don't know what it's like to really be kicked till you've had Bane's foot on your back...or maybe his knee! Baaaaaahahahaha!",
            value="", inline=True)
        embed.add_field(
            name="I'm only joking! But honestly, Bats really should learn to....watch his back....Nyaaaaahahahahahahaha.",
            value="", inline=True)
        embed.set_footer(
            text="For real though, we just want to sincerely apologize for anyone who may have accidentally been kicked. We were checking some member info in the member listings, specifically regarding activity, and unfortunately that info is listed in the same window as the \"prune\" function. A misclick occurred and *quite* a few of you were boop'd. We all know tech derps sometimes happen, but we want to once more sincerely apologize and hope no one was offended or hurt by it.")
        await ctx.channel.send(embed=embed)


def setup(bot):
    cog = Customs(bot)
    bot.add_cog(cog)
