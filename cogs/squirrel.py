import discord
from discord.ext import commands
from cogs.base_cog import BaseCog
from nyalib.NyaBot import ThrowawayException


class Squirrel(BaseCog):
    async def cog_before_invoke(self, ctx):
        if ctx.invoked_subcommand is not None:
            squirrel_role = discord.utils.get(ctx.guild.roles, id=329409494478094336)
            if squirrel_role is None:
                await ctx.reply('There is no Squirrel Army role on this server.')
                raise ThrowawayException

            squirrel_channel = ctx.guild.get_channel(self.config.bot.channel.squirrel)
            if squirrel_channel is None:
                await ctx.reply('The Squirrel Army channel cannot be found')
                raise ThrowawayException

            if not ctx.args:
                await ctx.reply('You need to provide a user to act on')
                raise ThrowawayException

            future_squirrel = ctx.args[0]
            if not future_squirrel:
                await ctx.reply('The user {} cannot be found'.format(future_squirrel.name))
                raise ThrowawayException

            ctx.squirrel_channel = squirrel_channel
            ctx.squirrel_role = squirrel_role

    @commands.group(invoke_without_command=True)
    async def squi(self, ctx):
        """Squirrel commands."""
        await ctx.invoke(self.bot.get_command("help"), ctx.invoked_with)

    @squi.command(description='Adds a user to the Squirrel Army.')
    @commands.guild_only()
    @commands.has_any_role('Nixie', 'Supervisors', 'Moderators', 'Elder Squirrels')
    async def add(self, ctx, future_squirrel: discord.Member = None):
        """Adds a user to the Squirrel Army"""
        if ctx.squirrel_role in future_squirrel.roles:
            await ctx.reply('The user {} is already a Squirrel'.format(future_squirrel.name))
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
            await ctx.reply('The user {} is not a Squirrel'.format(future_squirrel.name))
            return
        await future_squirrel.remove_roles(ctx.squirrel_role)
        await ctx.squirrel_channel.send('The user **{}** is no longer a squirrel.'.format(future_squirrel.name))


def setup(bot):
    cog = Squirrel(bot)
    bot.add_cog(cog)
