import discord
from discord.ext import commands
from nyalib.NyaBot import ThrowawayException
import random
from cogs.base_cog import BaseCog


class Giveaway(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.giveaways = {}

    async def cog_before_invoke(self, ctx):
        ctx.bot_channel = self.bot.get_channel(332644650462478336)
        if ctx.bot_channel is None:
            await ctx.channel.send('The dedicated bot commands channel cannot be found')
            raise ThrowawayException

        if ctx.invoked_subcommand.name != "list":
            giveaway_name = ctx.args[0]
            ctx.ga_role = discord.utils.get(giveaway_name)
            if ctx.ga_role is None:
                message = 'The giveaway "{}" doesn\'t exist, {}.'
                if ctx.invoked_subcommand.name == "start":
                    message = 'The giveaway "{}" already exists, {}.'
                await ctx.channel.send(message.format(giveaway_name, ctx.author.mention))
                raise ThrowawayException

    @commands.group(invoke_without_command=True)
    async def ga(self, ctx):
        """Giveaway commands."""
        await ctx.invoke(self.bot.get_command("help"), ctx.invoked_with)

    @ga.command(description='Starts a giveaway.')
    @commands.guild_only()
    @commands.has_any_role('Nixie', 'Supervisors',  'Moderators')
    async def start(self, ctx, giveaway_name: str):
        """Starts a giveaway"""
        self.giveaways[giveaway_name] = []
        await ctx.guild.create_role(name="giveaway_{}".format(giveaway_name), mentionable=True,
                                    reason="Give away started by {}".format(ctx.author.name))
        await ctx.channel.send(
            '**A new giveaway has started !**\n'
            'Please use the following commands to enter / leave this giveaway\n'
            '```!n.ga enter {0}``````!n.ga leave {0}```'.format(giveaway_name))

    @ga.command(description='Stop a giveaway.')
    @commands.guild_only()
    @commands.has_any_role('Nixie', 'Supervisors', 'Moderators')
    async def stop(self, ctx, giveaway_name: str):
        """Stop a giveaway"""
        # Remove the role from people
        for participant in ctx.ga_role.members:
            await participant.remove_roles(ctx.ga_role, reason="Give away stopped by {}".format(ctx.author.name))
        # Remove the role from server
        del self.giveaways[giveaway_name]
        await ctx.ga_role.delete()
        await ctx.channel.send(
            '**The giveaway "{}" has now ended, thank you all for your participation !**'.format(giveaway_name))

    @ga.command(description='List giveaways.')
    @commands.guild_only()
    async def list(self, ctx):
        """List giveaways"""
        ga_roles = [
            x.name.replace('giveaway_', '')
            for x in ctx.guild.roles
            if x.name.startswith('giveaway_')
        ]
        if not ga_roles:
            await ctx.bot_channel.send('There is no active giveaways, {}.'.format(ctx.author.mention))
            return
        await ctx.bot_channel.send(
            'Here is the list of the active giveaways ({}) :\n```{}```'.format(
                len(ga_roles), ", ".join(ga_roles)
            )
        )

    @ga.command(description='Enters a giveaway.')
    @commands.guild_only()
    async def enter(self, ctx, giveaway_name: str):
        """Enters a giveaway"""
        roles = ctx.author.roles
        has_role = discord.utils.get(roles, id=ctx.ga_role.id) is not None
        if has_role is not False:
            await ctx.bot_channel.send(
                'You already are in the giveaway "{}", {}'.format(giveaway_name, ctx.author.mention)
            )
            return

        await ctx.author.add_roles(ctx.ga_role)
        await ctx.bot_channel.send('You just entered the giveaway "{}", {}'.format(giveaway_name, ctx.author.mention))

    @ga.command(description='Leaves a giveaway.')
    @commands.guild_only()
    async def leave(self, ctx, giveaway_name: str):
        """Leaves a giveaway"""
        roles = ctx.author.roles
        has_role = discord.utils.get(roles, id=ctx.ga_role.id) is not None
        if has_role is False:
            await ctx.bot_channel.send('You are not in the giveaway "{}", {}'.format(giveaway_name, ctx.author.mention))
            return

        await ctx.author.remove_roles(ctx.ga_role)
        await ctx.bot_channel.send('You just left the giveaway "{}", {}'.format(giveaway_name, ctx.author.mention))

    @ga.command(description='Pick a winner from the people who entered the giveaway')
    @commands.guild_only()
    @commands.has_any_role('Nixie', 'Supervisors', 'Moderators')
    async def pick(self, ctx, giveaway_name: str):
        """Pick a winner"""
        participants = ctx.ga_role.members
        if not participants:
            await ctx.bot_channel.send('Nobody entered the giveaway "{}", {}.'.format(giveaway_name, ctx.author.mention))
            return

        updated_participants = [
            participant
            for participant in participants
            if participant.id not in self.giveaways[giveaway_name]
        ]
        if not updated_participants:
            await ctx.bot_channel.send(
                'Every participants already won the giveaway "{}", {}.'.format(giveaway_name, ctx.author.mention))
            return
        winner = random.choice(updated_participants)
        self.giveaways[giveaway_name].append(winner.id)
        await ctx.channel.send(
            '**Congratulation, {}, you just won in the giveaway "{}".'.format(winner.mention, giveaway_name))

    @ga.command(description='List winners ID')
    @commands.guild_only()
    @commands.has_any_role('Nixie', 'Supervisors', 'Moderators')
    async def winners(self, ctx, giveaway_name: str):
        """List winners ID"""
        winners = []
        for winner_id in self.giveaways[giveaway_name]:
            winner = self.bot.get_user(winner_id)
            if winner is not None:
                winners.append(winner.mention)

        if not winners:
            await ctx.bot_channel.send(
                'There is no winners for the giveaway "{}" yet, {}.'.format(giveaway_name, ctx.author.mention))
            return
        await ctx.bot_channel.send('List of winner :\n{}'.format("\n".join(str(x) for x in winners)))


def setup(bot):
    cog = Giveaway(bot)
    bot.add_cog(cog)
