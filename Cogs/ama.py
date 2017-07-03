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
        nb_message = 0
        nb_deleted = 0
        async for msg in ctx.channel.history(limit=None):
            nb_message += 1
            to_delete = False
            for reaction in msg.reactions:
                print(reaction.emoji.name)
                print(reaction.me)
                if reaction.emoji.name == 'downvote' and reaction.me:
                    to_delete = True
            if to_delete:
                nb_deleted += 1
                await msg.delete()
        await ctx.channel.send('{}/{} messages deleted.'.format(nb_deleted, nb_message))

    @commands.command(description='')
    @commands.guild_only()
    async def processq(self, ctx):
        """"""



def setup(bot):
    cog = Ama(bot)
    bot.add_cog(cog)
