import discord
from discord.ext import commands
from cogs.base_cog import BaseCog


class Cog(BaseCog, name="Channel"):
    @commands.group(invoke_without_command=True)
    async def channel(self, ctx):
        """Text Channel edition commands."""
        await ctx.send_help("channel")

    @channel.group(description='Create new channels with Supervisor permission.', invoke_without_command=True)
    @commands.has_any_role('Nixie', 'Supervisors')
    @commands.guild_only()
    async def create(self, ctx):
        await ctx.send_help("channel create")

    @create.command(description='Create a new text channel with Supervisor permission.')
    @commands.has_any_role('Nixie', 'Supervisors')
    @commands.guild_only()
    async def text(self, ctx, *, channel_name: str):
        """Create a new text channel with Supervisor permission."""
        if discord.utils.get(ctx.guild.text_channels, name=channel_name) is not None:
            await ctx.reply(f'Channel **{channel_name}** already exists')
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
        await ctx.reply(f"Created text channel {channel_name}")

    @create.command(description='Create a new voice channel with Supervisor permission.')
    @commands.has_any_role('Nixie', 'Supervisors')
    @commands.guild_only()
    async def voice(self, ctx, *, channel_name: str):
        """Create a new voice channel with Supervisor permission."""
        if discord.utils.get(ctx.guild.voice_channels, name=channel_name):
            await ctx.reply(f'Channel **{channel_name}** already exists, {ctx.author.mention}')
            return

        supervisor_role = discord.utils.get(ctx.guild.roles, name="Supervisors")
        if supervisor_role is None:
            await ctx.reply("Supervisor role is required to create")
            return

        perms = {
            supervisor_role: discord.PermissionOverwrite(manage_roles=True)
        }
        await ctx.guild.create_voice_channel(channel_name, overwrites=perms)
        await ctx.reply(f"Created text channel {channel_name}")
