import discord
from discord.ext import commands
import pymysql
import role_ids
from __main__ import config

class Nsfw():
    """Gives functions for the pervs out there ;-)"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Grabs the last picture from Konachan that matches your keywords.')
    @commands.guild_only()
    async def kona(self, ctx, *tags):
        """Grabs the last picture from Konachan that matches your keywords."""
        member = ctx.message.author
        try:
            await member.send('test')
        except:
            pass

def setup(bot):
    cog = Nsfw(bot)
    bot.add_cog(cog)

