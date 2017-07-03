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
        async for msg in ctx.channel.history(limit=None):
            to_delete = False
            for reaction in msg.reactions:
                if reaction.emoji == ':downvote:' and reaction.me:
                    to_delete = True
            if to_delete:
                await msg.delete()

    @commands.command(description='')
    @commands.guild_only()
    async def processq(self, ctx):
        """"""



def setup(bot):
    cog = Ama(bot)
    bot.add_cog(cog)
