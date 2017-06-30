from discord.ext import commands
import asyncio
import datetime
import role_ids

class Misc():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Pat Nya Chan.')
    @commands.guild_only()
    async def pat(self, ctx, location : str = 'head'):
        """Pat Nya Chan"""
        if location in ['head', 'back', 'belly', 'tummy']:
            msg = 'Nyaaaaaah, Thank you {} =^.^='.format(ctx.message.author.mention)
        elif location in ['boobs', 'ass', 'butt']:
            msg = 'Eeeeeeeeeeek !!'
        else:
            return
        await ctx.channel.send(msg)

    @commands.command(description='Get the number of minutes to wait until Nixie\'s next steam.')
    @commands.guild_only()
    async def stream(self, ctx):
        """Get the number of minutes to wait until Nixie\'s next steam"""
        now = datetime.datetime.now()
        launch = datetime.datetime(2017, 6, 27, 22, 0, 0, 0)
        delta = launch - now
        minutes = round(delta.days * 24 * 60 + delta.seconds / 60 + delta.microseconds / 60000000)
        if minutes > 0:
            await ctx.channel.send("{} minutes until Nixie's next stream, YAY !".format(minutes))
        elif minutes > -60:
            await ctx.channel.send("Stream in progress ... hopefully, have fun !")
        else:
            await ctx.channel.send("Stay tuned, next stream date will be announced soon !")

def setup(bot):
    cog = Misc(bot)
    bot.add_cog(cog)
