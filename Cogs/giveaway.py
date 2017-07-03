from discord.ext import commands
import asyncio
import datetime
import role_ids

class Giveaway():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Start a giveaway.')
    @commands.guild_only()
    @commands.has_any_role('Nixie', 'Mods')
    async def startgiveaway (self, ctx, ga_name: str):
        """Start a giveaway"""
        ga_role = await self.bot.create_role(name="giveaway_{}".format(ga_name), mentionable=True, reason="Give away started by {}".format(ctx.author.name))
        await ctx.channel.send('**A new giveaway has started !**\nPlease use the following command to enter / leave this giveaway\n```!n.giveaway {}```'.format(ga_name))
        
    @commands.command(description='Enter/Leave a giveaway.')
    @commands.guild_only()
    async def giveaway (self, ctx, ga_name: str):
        ga_role = None        
        for x in ctx.guild.roles:
            if x.name == 'giveaway_{}'.format(ga_name):
                ga_role = x
        if ga_role == None:
            await ctx.channel.send('The giveaway "{}" doesn\'t exist, {}.'.format(ga_name, ctx.author.mention))
            return False
        roles = ctx.author.roles
        has_role = False
        for role in roles:
            if role.id == ga_role.id:
                has_role = True
        if has_role == False:
            await ctx.author.add_roles(ga_role)
            await ctx.channel.send('You just entered the giveaway "{}", {}'.format(ga_name, ctx.author.mention))
        else:
            await ctx.author.remove_roles(ga_role)
            await ctx.channel.send('You just left the giveaway "{}", {}'.format(ga_name, ctx.author.mention))

def setup(bot):
    cog = Giveaway(bot)
    bot.add_cog(cog)
