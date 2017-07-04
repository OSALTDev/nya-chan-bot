from discord.ext import commands
import random
from cogs.base_cog import BaseCog

class Giveaway(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.giveaways = {}

    @commands.command(description='Start a giveaway.')
    @commands.guild_only()
    @commands.has_any_role('Nixie', 'Mods')
    async def startgiveaway (self, ctx, giveaway_name: str):
        """Start a giveaway"""
        ga_role = None        
        for x in ctx.guild.roles:
            if x.name == 'giveaway_{}'.format(giveaway_name):
                ga_role = x
        if not ga_role == None:
            await ctx.channel.send('The giveaway "{}" already exists, {}.'.format(giveaway_name, ctx.author.mention))
            return False
        self.giveaways[giveaway_name] = []
        ga_role = await ctx.guild.create_role(name="giveaway_{}".format(giveaway_name), mentionable=True, reason="Give away started by {}".format(ctx.author.name))
        await ctx.channel.send('**A new giveaway has started !**\nPlease use the following command to enter / leave this giveaway\n```!n.giveaway {}```'.format(giveaway_name))

    @commands.command(description='Stop a giveaway.')
    @commands.guild_only()
    @commands.has_any_role('Nixie', 'Mods')
    async def stopgiveaway (self, ctx, giveaway_name: str):
        """Stop a giveaway"""
        ga_role = None        
        for x in ctx.guild.roles:
            if x.name == 'giveaway_{}'.format(giveaway_name):
                ga_role = x
        if ga_role == None:
            await ctx.channel.send('The giveaway "{}" doesn\'t exist, {}.'.format(giveaway_name, ctx.author.mention))
            return False
        #Remove the role from people
        for participant in ga_role.members:
            await participant.remove_roles(ga_role, reason="Give away stopped by {}".format(ctx.author.name))
        #Remove the role from server
        del self.giveaways[giveaway_name]
        await ga_role.delete()
        await ctx.channel.send('**The giveaway "{}" has now ended, thank you all for your participation !**'.format(giveaway_name))

    @commands.command(description='List giveaways.')
    @commands.guild_only()
    async def listgiveaways (self, ctx):
        """List giveaways"""
        ga_roles = []        
        for x in ctx.guild.roles:
            if x.name.startswith('giveaway_'):
                ga_roles.append(x.name.replace('giveaway_', ''))
        if len(ga_roles) == 0:
            await ctx.channel.send('There is no active giveaways, {}.'.format(ctx.author.mention))
            return False
        await ctx.channel.send('Here is the list of the active giveaways ({}) :\n```{}```'.format(len(ga_roles), ", ".join(str(x) for x in ga_roles)))
        
    @commands.command(description='Enter/Leave a giveaway.')
    @commands.guild_only()
    async def giveaway (self, ctx, giveaway_name: str):
        """Enter/Leave a giveaway"""
        ga_role = None        
        for x in ctx.guild.roles:
            if x.name == 'giveaway_{}'.format(giveaway_name):
                ga_role = x
        if ga_role == None:
            await ctx.channel.send('The giveaway "{}" doesn\'t exist, {}.'.format(giveaway_name, ctx.author.mention))
            return False
        roles = ctx.author.roles
        has_role = False
        for role in roles:
            if role.id == ga_role.id:
                has_role = True
        if has_role == False:
            await ctx.author.add_roles(ga_role)
            await ctx.channel.send('You just entered the giveaway "{}", {}'.format(giveaway_name, ctx.author.mention))
        else:
            await ctx.author.remove_roles(ga_role)
            await ctx.channel.send('You just left the giveaway "{}", {}'.format(giveaway_name, ctx.author.mention))

    @commands.command(description='Pick a winner from the people who entered the giveaway')
    @commands.guild_only()
    @commands.has_any_role('Nixie', 'Mods')
    async def pickwinner(self, ctx, giveaway_name : str):
        """Pick a winner"""
        ga_role = None
        for x in ctx.guild.roles:
            if x.name == 'giveaway_{}'.format(giveaway_name):
                ga_role = x
        if ga_role == None:
            await ctx.channel.send('The giveaway "{}" doesn\'t exist, {}.'.format(giveaway_name, ctx.author.mention))
            return False
        participants = ga_role.members
        if len(participants) == 0:
            await ctx.channel.send('Nobody entered the giveaway "{}", {}.'.format(giveaway_name, ctx.author.mention))
            return False
        updated_participants = []
        for participant in participants:
            if not participant.id in self.giveaways[giveaway_name]:
                updated_participants.append(participant)
        if len(updated_participants) == 0:
            await ctx.channel.send('Every participants already won the giveaway "{}", {}.'.format(giveaway_name, ctx.author.mention))
            return False
        winner = random.choice(updated_participants)
        self.giveaways[giveaway_name].append(winner.id)
        await ctx.channel.send('**Congratulation, {}, you just won in the giveaway "{}".'.format(winner.mention, giveaway_name))

    @commands.command(description='List winners ID')
    @commands.guild_only()
    @commands.has_any_role('Nixie', 'Mods')
    async def listwinners(self, ctx, giveaway_name : str):
        """List winners ID"""
        ga_role = None
        for x in ctx.guild.roles:
            if x.name == 'giveaway_{}'.format(giveaway_name):
                ga_role = x
        if ga_role == None:
            await ctx.channel.send('The giveaway "{}" doesn\'t exist, {}.'.format(giveaway_name, ctx.author.mention))
            return False
        winners = []
        for winner_id in self.giveaways[giveaway_name]:
            winner = self.bot.get_user(winner_id)
            if not winner is None:
                winners.append(winner.mention)
        if len(winners) == 0:
            await ctx.channel.send('There is no winners for the giveaway "{}" yet, {}.'.format(giveaway_name, ctx.author.mention))
            return False
        await ctx.channel.send('List of winner :\n{}'.format("\n".join(str(x) for x in winners)))

def setup(bot):
    cog = Giveaway(bot)
    bot.add_cog(cog)
