import discord
from discord.ext import commands
from discord.ext.commands import group
from cogs.base_cog import BaseCog


class Vchannels(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)

    @group()
    async def vch(self, ctx):
        """Voice Channel edition commands."""
        if ctx.invoked_subcommand is None:
            await self.bot_reply(ctx, 'Invalid Voice Channel Edition command passed, {}'.format(ctx.author.mention))

    @vch.command(description='Create a new voice channel with Supervisor permission.')
    @commands.has_any_role('Nixie', 'Supervisors')
    @commands.guild_only()
    async def create(self, ctx, *, channel_name: str):
        """Create a new voice channel with Supervisor permission."""
        if discord.utils.get(ctx.guild.voice_channels, name=channel_name):
            await self.bot_reply(ctx, 'Channel **{}** already exists, {}'.format(channel_name, ctx.author.mention))
            return

        supervisor_role = discord.utils.get(ctx.guild.roles, name="Supervisors")
        if supervisor_role is None:
            return

        perms = {
            supervisor_role: discord.PermissionOverwrite(manage_roles=True)
        }
        await ctx.guild.create_voice_channel(channel_name, overwrites=perms)


def setup(bot):
    cog = Vchannels(bot)
    bot.add_cog(cog)
