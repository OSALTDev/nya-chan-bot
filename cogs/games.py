import discord
from discord.ext import commands
from cogs.base_cog import BaseCog


class Cog(BaseCog, name="Games"):
    @commands.command(description='Identify yourself as looking for a game (toggle command).')
    @commands.guild_only()
    async def lfg(self, ctx):
        """Toggle your LFG status"""
        lfg_role = discord.utils.get(ctx.guild.roles, name="LFG")
        if lfg_role is None:
            await ctx.channel.send('There is no LFG role on this server.')
            return

        has_role = discord.utils.get(ctx.author.roles, name="LFG") is not None
        if has_role is False:
            await ctx.author.add_roles(lfg_role)
            await ctx.channel.send('You are now tagged as looking for a game, {}'.format(ctx.author.mention))
        else:
            await ctx.author.remove_roles(lfg_role)
            await ctx.channel.send('You are not tagged as looking for a game anymore, {}'.format(ctx.author.mention))
