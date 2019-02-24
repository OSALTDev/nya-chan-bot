import discord
from discord.ext import commands
from discord.ext.commands import group
from cogs.base_cog import BaseCog


class Channels(BaseCog):
    @group()
    async def channel(self, ctx):
        """Text Channel edition commands."""
        if ctx.invoked_subcommand is None:
            await ctx.reply('Invalid Text Channel Edition command passed')

    @channel.command(description='Create a new text channel with Supervisor permission.')
    @commands.has_any_role('Nixie', 'Supervisors')
    @commands.guild_only()
    async def create(self, ctx, *, channel_name: str):
        """Create a new text channel with Supervisor permission."""
        if discord.utils.get(ctx.guild.text_channels, name=channel_name) is not None:
            await ctx.reply('Channel **{}** already exists'.format(channel_name))
            return

        supervisor_role = discord.utils.get(ctx.guild.roles, name="Supervisors")
        if supervisor_role is None:
            await ctx.reply("Supervisor role is required to create")
            return

        perms = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            supervisor_role: discord.PermissionOverwrite(read_messages=True, manage_roles=True)
        }
        await ctx.guild.create_text_channel(channel_name, overwrites=perms)
        await ctx.reply("Created text channel {}".format(channel_name))


def setup(bot):
    cog = Channels(bot)
    bot.add_cog(cog)
