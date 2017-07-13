from discord.ext import commands
from discord.ext.commands import group
from cogs.base_cog import BaseCog


class Squirrel(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)

    def get_squirrel_role(self, ctx):
        for role in ctx.guild.roles:
            if role.id == 329409494478094336:
                return role
        return None

    @group()
    async def squi(self, ctx):
        """Squirrel commands."""
        bot_channel = self.bot.get_channel(332644650462478336)
        if bot_channel is None:
            await ctx.channel.send('The dedicated bot commands channel cannot be found')
            return False
        if ctx.invoked_subcommand is None:
            await bot_channel.send('Invalid squirrel command passed, {}'.format(ctx.author.mention))

    @squi.command(description='Adds a user to the Squirrel Army.')
    @commands.guild_only()
    @commands.has_any_role('Nixie', 'Mods', 'Elder Squirrel')
    async def add(self, ctx, username: str):
        """Adds a user to the Squirrel Army"""
        bot_channel = self.bot.get_channel(332644650462478336)
        if bot_channel is None:
            await ctx.channel.send('The dedicated bot commands channel cannot be found')
            return False
        squirrel_role = self.get_squirrel_role(ctx)
        if squirrel_role is None:
            await bot_channel.send('There is no Squirrel Army role on this server.')
            return False
        converter = commands.converter.MemberConverter()
        future_squirrel = await converter.convert(ctx, username)
        if future_squirrel is None:
            await bot_channel.send('The user {} cannot be found'.format(username))
            return False
        squirrel_channel = self.bot.get_channel(329379656576794625)
        if squirrel_channel is None:
            await bot_channel.send('The Squirrel Army channel cannot be found')
            return False
        if squirrel_role in future_squirrel.roles:
            await bot_channel.send('The user {} is already a Squirrel'.format(username))
            return False
        await future_squirrel.add_roles(squirrel_role)
        await squirrel_channel.send(
            'Welcome to the Squirrel Army {}, happy squirreling =^.^='.format(future_squirrel.mention))

    @squi.command(description='Removes a user from the Squirrel Army.')
    @commands.guild_only()
    @commands.has_any_role('Nixie', 'Mods', 'Elder Squirrel')
    async def remove(self, ctx, username: str):
        """Removes a user from the Squirrel Army"""
        bot_channel = self.bot.get_channel(332644650462478336)
        if bot_channel is None:
            await ctx.channel.send('The dedicated bot commands channel cannot be found')
            return False
        squirrel_role = self.get_squirrel_role(ctx)
        if squirrel_role is None:
            await bot_channel.send('There is no Squirrel Army role on this server.')
            return False
        converter = commands.converter.MemberConverter()
        future_squirrel = await converter.convert(ctx, username)
        if future_squirrel is None:
            await bot_channel.send('The user {} cannot be found'.format(username))
            return False
        squirrel_channel = self.bot.get_channel(329379656576794625)
        if squirrel_channel is None:
            await bot_channel.send('The Squirrel Army channel cannot be found')
            return False
        if squirrel_role not in future_squirrel.roles:
            await bot_channel.send('The user {} is not a Squirrel'.format(username))
            return False
        await future_squirrel.remove_roles(squirrel_role)
        await squirrel_channel.send('The user **{}** is no longer a squirrel.'.format(future_squirrel.name))


def setup(bot):
    cog = Squirrel(bot)
    bot.add_cog(cog)
