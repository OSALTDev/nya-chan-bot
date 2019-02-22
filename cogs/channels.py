import discord
from discord.ext import commands
from discord.ext.commands import group
from cogs.base_cog import BaseCog


class Channels(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)

    @group()
    async def tch(self, ctx):
        """Text Channel edition commands."""
        if ctx.invoked_subcommand is None:
            await self.bot_reply(ctx, 'Invalid Text Channel Edition command passed, {}'.format(ctx.author.mention))

    @tch.command(description='Create a new text channel with Supervisor permission.')
    @commands.has_any_role('Nixie', 'Supervisors')
    @commands.guild_only()
    async def create(self, ctx, *, channel_name: str):
        """Create a new text channel with Supervisor permission."""
        guild = ctx.guild
        if discord.utils.get(guild.text_channels, name=channel_name) is not None:
            await self.bot_reply(ctx, 'Channel **{}** already exists, {}'.format(channel_name, ctx.author.mention))
            return False
        supervisor_role = discord.utils.get(guild.roles, name="Supervisors")
        if supervisor_role is None:
            return False
        perms = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            supervisor_role: discord.PermissionOverwrite(read_messages=True, manage_roles=True)
        }
        await guild.create_text_channel(channel_name, overwrites=perms)


def setup(bot):
    cog = Channels(bot)
    bot.add_cog(cog)
