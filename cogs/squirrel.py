import discord
from discord.ext import commands
from cogs.base_cog import BaseCog
from nyalib.NyaBot import ThrowawayException


class Cog(BaseCog, name="Squirrel"):
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

            ctx.custom["squirrel_channel"] = squirrel_channel
            ctx.custom["squirrel_role"] = squirrel_role

    @commands.group(invoke_without_command=True)
    async def squi(self, ctx):
        """Squirrel commands."""
        await ctx.send_help("squi")

    @squi.command(description='Adds a user to the Squirrel Army.')
    @commands.guild_only()
    @commands.has_any_role('Nixie', 'Supervisors', 'Moderators', 'Elder Squirrels')
    async def add(self, ctx, future_squirrel: discord.Member):
        """Adds a user to the Squirrel Army"""
        if ctx.custom.squirrel_role in future_squirrel.roles:
            await ctx.reply(f'The user {future_squirrel.name} is already a Squirrel')
            return
        await future_squirrel.add_roles(ctx.custom.squirrel_role)
        await ctx.custom.squirrel_channel.send(f'Welcome to the Squirrel Army {future_squirrel.name}, '
                                               'happy squirreling =^.^=')

    @squi.command(description='Removes a user from the Squirrel Army.')
    @commands.guild_only()
    @commands.has_any_role('Nixie', 'Supervisors', 'Moderators', 'Elder Squirrels')
    async def remove(self, ctx, future_squirrel: discord.Member):
        """Removes a user from the Squirrel Army"""
        if ctx.custom.squirrel_role not in future_squirrel.roles:
            await ctx.reply(f'The user {future_squirrel.name} is not a Squirrel')
            return
        await future_squirrel.remove_roles(ctx.custom.squirrel_role)
        await ctx.custom.squirrel_channel.send(f'The user **{future_squirrel.name}** is no longer a squirrel.')
