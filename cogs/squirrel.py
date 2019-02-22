import discord
from discord.ext import commands
from discord.ext.commands import group
from cogs.base_cog import BaseCog
from nyalib.NyaBot import ThrowawayException


class Squirrel(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)

    def _Squirrel__before_invoke(self, ctx):
        bot_channel = ctx.guild.get_channel(332644650462478336)
        if bot_channel is None:
            await ctx.channel.send('The dedicated bot commands channel cannot be found')
            raise ThrowawayException

        ctx.bot_channel = bot_channel

        if ctx.invoked_subcommand is not None:
            squirrel_role = discord.utils.get(ctx.guild.roles, id=329409494478094336)
            if squirrel_role is None:
                await bot_channel.send('There is no Squirrel Army role on this server.')
                raise ThrowawayException

            squirrel_channel = ctx.guild.get_channel(329379656576794625)
            if squirrel_channel is None:
                await bot_channel.send('The Squirrel Army channel cannot be found')
                raise ThrowawayException

            if not ctx.args:
                await bot_channel.send('You need to provide a user to act on')
                raise ThrowawayException

            future_squirrel = ctx.args[0]
            if not future_squirrel:
                await bot_channel.send('The user {} cannot be found'.format(future_squirrel.name))
                raise ThrowawayException

            ctx.squirrel_channel = squirrel_channel
            ctx.squirrel_role = squirrel_role

    @group()
    async def squi(self, ctx):
        """Squirrel commands."""
        if ctx.invoked_subcommand is None:
            await ctx.bot_channel.send('Invalid squirrel command passed, {}'.format(ctx.author.mention))

    @squi.command(description='Adds a user to the Squirrel Army.')
    @commands.guild_only()
    @commands.has_any_role('Nixie', 'Supervisors', 'Moderators', 'Elder Squirrels')
    async def add(self, ctx, future_squirrel: discord.Member = None):
        """Adds a user to the Squirrel Army"""
        if ctx.squirrel_role in future_squirrel.roles:
            await ctx.bot_channel.send('The user {} is already a Squirrel'.format(future_squirrel.name))
            return
        await future_squirrel.add_roles(ctx.squirrel_role)
        await ctx.squirrel_channel.send(
            'Welcome to the Squirrel Army {}, happy squirreling =^.^='.format(future_squirrel.mention))

    @squi.command(description='Removes a user from the Squirrel Army.')
    @commands.guild_only()
    @commands.has_any_role('Nixie', 'Supervisors', 'Moderators', 'Elder Squirrels')
    async def remove(self, ctx, future_squirrel: discord.Member = None):
        """Removes a user from the Squirrel Army"""
        if ctx.squirrel_role not in future_squirrel.roles:
            await ctx.bot_channel.send('The user {} is not a Squirrel'.format(future_squirrel.name))
            return
        await future_squirrel.remove_roles(ctx.squirrel_role)
        await ctx.squirrel_channel.send('The user **{}** is no longer a squirrel.'.format(future_squirrel.name))


def setup(bot):
    cog = Squirrel(bot)
    bot.add_cog(cog)
