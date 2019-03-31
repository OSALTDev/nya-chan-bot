from discord.ext import commands
import datetime
from cogs.base_cog import BaseCog


class Cog(BaseCog, name="Misc"):
    @commands.command(description='Pat Nya Chan.')
    @commands.guild_only()
    async def pat(self, ctx, location: str = 'head'):
        """Pat Nya Chan"""
        if location in ['head', 'back', 'belly', 'tummy']:
            msg = 'Nyaaaaaah, Thank you {} =^.^='.format(ctx.message.author.mention)
        elif location in ['boobs', 'ass', 'butt']:
            msg = 'Eeeeeeeeeeek !!'
        else:
            return
        await ctx.channel.send(msg)

    @commands.command(description='Get the number of minutes to wait until Nixie\'s next stream.')
    @commands.guild_only()
    async def stream(self, ctx):
        """Get the number of minutes to wait until Nixie\'s next stream"""
        now = datetime.datetime.now()
        # TODO : move that out of the main code
        launch = datetime.datetime(2017, 7, 9, 22, 0, 0, 0)
        delta = launch - now
        minutes = round(delta.days * 24 * 60 + delta.seconds / 60 + delta.microseconds / 60000000)
        if minutes > 0:
            await ctx.channel.send("```{} minutes until Nixie's next stream, YAY !```".format(minutes))
        elif minutes > -60:
            await ctx.channel.send("```Stream in progress ... hopefully, have fun !```")
        else:
            await ctx.channel.send("```Stay tuned, next stream date will be announced soon !```")

    @commands.command(description='Says how many people are on this Discord')
    @commands.guild_only()
    @commands.has_any_role('Nixie', 'Supervisors', 'GeeksAbroad')
    async def servercount(self, ctx):
        """Says how many people are on this Discord"""
        await ctx.reply('There are **{}** members on this Discord'.format(len(ctx.guild.members)))
