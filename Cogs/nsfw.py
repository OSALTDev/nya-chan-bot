import discord
from discord.ext import commands
from urllib import parse
import os
import aiohttp
from __main__ import config

class Nsfw():
    """Gives functions for the pervs out there ;-)"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Grabs the last picture from Konachan that matches your keywords.')
    @commands.guild_only()
    async def kona(self, ctx, *tags):
        """Grabs the last picture from Konachan that matches your keywords."""
        await fetch_image(self, ctx, randomize=False, tags=tags)

    async def fetch_image(self, ctx, randomize : bool=False, tags : list=[]):
        guild = ctx.message.guild
        search = "https://konachan.com/post.json?limit=1&tags="
        tag_search = "{} ".format(" ".join(tags))
        if randomize:
            tag_search += " order:random"
        search += parse.quote_plus(tagSearch)
        message = await ctx.send("Fetching kona image...")






def setup(bot):
    cog = Nsfw(bot)
    bot.add_cog(cog)

