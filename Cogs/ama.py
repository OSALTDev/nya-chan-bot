from discord.ext import commands
import asyncio
import datetime
import role_ids

class Ama():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='')
    @commands.guild_only()
    async def copyq(self, ctx):
        """Copy every question with your :upvote: reaction on it to the Question- channel"""
        
        
    @commands.command(description='')
    @commands.guild_only()
    async def cleanq(self, ctx):
        """Delete every message with your :downvote: reaction"""

    @commands.command(description='')
    @commands.guild_only()
    async def processq(self, ctx):
        """"""



def setup(bot):
    cog = Ama(bot)
    bot.add_cog(cog)
