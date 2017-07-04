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
        lfg_role = None
        for x in ctx.guild.roles:
            if x.name == 'LFG':
                lfg_role = x
        if lfg_role == None:
            await ctx.channel.send('There is no LFG role on this server.')
            return False
        roles = ctx.author.roles
        has_role = False
        for role in roles:
            if role.name == 'LFG':
                has_role = True
        if has_role == False:
            await ctx.author.add_roles(lfg_role)
            await ctx.channel.send('You are now tagged as looking for a game, {}'.format(ctx.author.mention))
        else:
            await ctx.author.remove_roles(lfg_role)
            await ctx.channel.send('You are not tagged as looking for a game anymore, {}'.format(ctx.author.mention))

def setup(bot):
    cog = Games(bot)
    bot.add_cog(cog)
