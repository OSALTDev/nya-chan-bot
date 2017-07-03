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
        nb_copied = 0
        destination = self.bot.get_channel(331363194780254210)
        if destination is None:
            await ctx.channel.send('There is no destination channel.')
            return False
        async for msg in ctx.channel.history(limit=200):
            to_copy = False
            for reaction in msg.reactions:
                from_me = False
                async for usr in reaction.users():
                    if usr.id == ctx.author.id:
                        from_me = True
                if reaction.emoji.name == 'upvote' and from_me is True:
                    to_copy = True
            if to_copy:
                nb_copied += 1
                await destination.send('From {} - {} UTC (Processed by {})\n-----------------------\n{}'.format(msg.author.mention, msg.created_at.strftime('%c'), ctx.author.mention, msg.content))
                await msg.delete()
        await ctx.channel.send('{} message(s) transferred to {}.'.format(nb_copied, destination.name))
                    
                      
        
    @commands.command(description='')
    @commands.guild_only()
    async def cleanq(self, ctx):
        """Delete every message with your :downvote: reaction"""
        nb_deleted = 0
        async for msg in ctx.channel.history(limit=200):
            to_delete = False
            for reaction in msg.reactions:
                from_me = False
                async for usr in reaction.users():
                    if usr.id == ctx.author.id:
                        from_me = True
                if reaction.emoji.name == 'downvote' and from_me is True:
                    to_delete = True
            if to_delete:
                nb_deleted += 1
                await msg.delete()
        await ctx.channel.send('{} message(s) have been processed.'.format(nb_deleted))

    @commands.command(description='')
    @commands.guild_only()
    async def processq(self, ctx):
        """"""



def setup(bot):
    cog = Ama(bot)
    bot.add_cog(cog)
