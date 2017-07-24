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
        embed.set_thumbnail(url='https://i.ytimg.com/vi/I9GcnRAdY2M/maxresdefault.jpg')
        embed.add_field(name="▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬",
                        value="**Joker here, with an announcement for all my lovely adoring fans here at Joker Asylum!**\n\n**You may have noticed we had some regulars having to rejoin this server, having been kicked!**\n\n**I just gotta say, ya don't know what it's like to really be kicked till you've had Bane's foot on your back...or maybe his knee! Baaaaaahahahaha!**\n\n**I'm only joking! Honestly, Bats really should learn to watch his back... Nyaaaaahahahahahaha.**",
                        inline=True)
        embed.set_footer(
            text="For real though, we just want to sincerely apologize for anyone who may have accidentally been kicked. We were checking some member info in the member listings, specifically regarding activity, and unfortunately that info is listed in the same window as the \"prune\" function. A misclick occurred and *quite* a few of you were boop'd. We all know tech derps sometimes happen, but we want to once more sincerely apologize and hope no one was offended or hurt by it.")
        await ctx.channel.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    @commands.guild_only()
    async def kicked(self, ctx):
        connection = self.config.db_connection()
        cursor = connection.cursor()
        cursor.execute("""SELECT DISTINCT `id_user` FROM `statistics_global`""")
        member_ids = cursor.fetchall()
        nb_kicked = 0
        for member_id in member_ids:
            member = ctx.guild.get_member(int(member_id[0]))
            if member is None:
                cursor.execute("""INSERT INTO `kicked` (`id`, `id_user`) VALUES (NULL, %s)""", member_id[0])
                connection.commit()
                nb_kicked += 1
        connection.close()
        await ctx.author.send('{} Users were kicked'.format(nb_kicked))


def setup(bot):
    cog = Customs(bot)
    bot.add_cog(cog)
