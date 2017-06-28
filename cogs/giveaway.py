from discord.ext import commands
from discord.ext.commands import group
import random
from cogs.base_cog import BaseCog


class Giveaway(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.giveaways = {}

    @group()
    async def ga(self, ctx):
        """Giveaway commands."""
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid giveaway command passed, {}'.format(ctx.author.mention))

    @ga.command(description='Starts a giveaway.')
    @commands.guild_only()
    @commands.has_any_role('Nixie', 'Mods')
    async def start(self, ctx, giveaway_name: str):
        """Starts a giveaway"""
        ga_role = None
        for x in ctx.guild.roles:
            if x.name == 'giveaway_{}'.format(giveaway_name):
                ga_role = x
        if ga_role is not None:
            await ctx.channel.send('The giveaway "{}" already exists, {}.'.format(giveaway_name, ctx.author.mention))
            return False
        self.giveaways[giveaway_name] = []
        ga_role = await ctx.guild.create_role(name="giveaway_{}".format(giveaway_name), mentionable=True,
                                              reason="Give away started by {}".format(ctx.author.name))
        await ctx.channel.send('**A new giveaway has started !**\nPlease use the following commands to enter / leave\
this giveaway\n```!n.ga enter {0}``````!n.ga leave {0}```'.format(giveaway_name))

    @ga.command(description='Stop a giveaway.')
    @commands.guild_only()
    @commands.has_any_role('Nixie', 'Mods')
    async def stop(self, ctx, giveaway_name: str):
        """Stop a giveaway"""
        ga_role = None
        for x in ctx.guild.roles:
            if x.name == 'giveaway_{}'.format(giveaway_name):
                ga_role = x
        if ga_role is None:
            await ctx.channel.send('The giveaway "{}" doesn\'t exist, {}.'.format(giveaway_name, ctx.author.mention))
            return False
        # Remove the role from people
        for participant in ga_role.members:
            await participant.remove_roles(ga_role, reason="Give away stopped by {}".format(ctx.author.name))
        # Remove the role from server
        del self.giveaways[giveaway_name]
        await ga_role.delete()
        await ctx.channel.send(
            '**The giveaway "{}" has now ended, thank you all for your participation !**'.format(giveaway_name))

    @ga.command(description='List giveaways.')
    @commands.guild_only()
    async def list(self, ctx):
        """List giveaways"""
        ga_roles = []
        for x in ctx.guild.roles:
            if x.name.startswith('giveaway_'):
                ga_roles.append(x.name.replace('giveaway_', ''))
        if len(ga_roles) == 0:
            await ctx.channel.send('There is no active giveaways, {}.'.format(ctx.author.mention))
            return False
        await ctx.channel.send('Here is the list of the active giveaways ({}) :\n```{}```'.format(len(ga_roles),
                                                                                                  ", ".join(
                                                                                                      str(x) for x in
                                                                                                      ga_roles)))

    @ga.command(description='Enters a giveaway.')
    @commands.guild_only()
    async def enter(self, ctx, giveaway_name: str):
        """Enters a giveaway"""
        ga_role = None
        for x in ctx.guild.roles:
            if x.name == 'giveaway_{}'.format(giveaway_name):
                ga_role = x
        if ga_role is None:
            await ctx.channel.send('The giveaway "{}" doesn\'t exist, {}.'.format(giveaway_name, ctx.author.mention))
            return False
        roles = ctx.author.roles
        has_role = False
        for role in roles:
            if role.id == ga_role.id:
                has_role = True
        if has_role is not False:
            await ctx.channel.send('You already are in the giveaway "{}", {}'.format(giveaway_name, ctx.author.mention))
            return False
        await ctx.author.add_roles(ga_role)
        await ctx.channel.send('You just entered the giveaway "{}", {}'.format(giveaway_name, ctx.author.mention))

    @ga.command(description='Leaves a giveaway.')
    @commands.guild_only()
    async def leave(self, ctx, giveaway_name: str):
        """Leaves a giveaway"""
        ga_role = None
        for x in ctx.guild.roles:
            if x.name == 'giveaway_{}'.format(giveaway_name):
                ga_role = x
        if ga_role is None:
            await ctx.channel.send('The giveaway "{}" doesn\'t exist, {}.'.format(giveaway_name, ctx.author.mention))
            return False
        roles = ctx.author.roles
        has_role = False
        for role in roles:
            if role.id == ga_role.id:
                has_role = True
        if has_role is False:
            await ctx.channel.send('You are not in the giveaway "{}", {}'.format(giveaway_name, ctx.author.mention))
            return False
        await ctx.author.remove_roles(ga_role)
        await ctx.channel.send('You just left the giveaway "{}", {}'.format(giveaway_name, ctx.author.mention))

    @ga.command(description='Pick a winner from the people who entered the giveaway')
    @commands.guild_only()
    @commands.has_any_role('Nixie', 'Mods')
    async def pick(self, ctx, giveaway_name: str):
        """Pick a winner"""
        ga_role = None
        for x in ctx.guild.roles:
            if x.name == 'giveaway_{}'.format(giveaway_name):
                ga_role = x
        if ga_role is None:
            await ctx.channel.send('The giveaway "{}" doesn\'t exist, {}.'.format(giveaway_name, ctx.author.mention))
            return False
        participants = ga_role.members
        if len(participants) == 0:
            await ctx.channel.send('Nobody entered the giveaway "{}", {}.'.format(giveaway_name, ctx.author.mention))
            return False
        updated_participants = []
        for participant in participants:
            if participant.id not in self.giveaways[giveaway_name]:
                updated_participants.append(participant)
        if len(updated_participants) == 0:
            await ctx.channel.send(
                'Every participants already won the giveaway "{}", {}.'.format(giveaway_name, ctx.author.mention))
            return False
        winner = random.choice(updated_participants)
        self.giveaways[giveaway_name].append(winner.id)
        await ctx.channel.send(
            '**Congratulation, {}, you just won in the giveaway "{}".'.format(winner.mention, giveaway_name))

    @ga.command(description='List winners ID')
    @commands.guild_only()
    @commands.has_any_role('Nixie', 'Mods')
    async def winners(self, ctx, giveaway_name: str):
        """List winners ID"""
        ga_role = None
        for x in ctx.guild.roles:
            if x.name == 'giveaway_{}'.format(giveaway_name):
                ga_role = x
        if ga_role is None:
            await ctx.channel.send('The giveaway "{}" doesn\'t exist, {}.'.format(giveaway_name, ctx.author.mention))
            return False
        winners = []
        for winner_id in self.giveaways[giveaway_name]:
            winner = self.bot.get_user(winner_id)
            if winner is not None:
                winners.append(winner.mention)
        if len(winners) == 0:
            await ctx.channel.send(
                'There is no winners for the giveaway "{}" yet, {}.'.format(giveaway_name, ctx.author.mention))
            return False
        await ctx.channel.send('List of winner :\n{}'.format("\n".join(str(x) for x in winners)))


def setup(bot):
    cog = Giveaway(bot)
    bot.add_cog(cog)
