from discord.ext import commands
import asyncio
import datetime
import role_ids

class Games():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Identify yourself as looking for a game (toggle command).')
    @commands.guild_only()
    async def lfg(self, ctx):
        """Toggle your LFG status"""
        roles = ctx.author.roles
        hasRole = False
        for role in roles:
            if role.name == 'LFG':
                hasRole = True
        if hasRole:
            await ctx.author.add_roles(['LFG'])
            await ctx.channel.send('You are now tagged as looking for a game, {}'.format(ctx.author.mention))
        else:
            await ctx.author.remove_roles(['LFG'])
            await ctx.channel.send('You are not tagged as looking for a game anymore, {}'.format(ctx.author.mention))

def setup(bot):
    cog = Games(bot)
    bot.add_cog(cog)
