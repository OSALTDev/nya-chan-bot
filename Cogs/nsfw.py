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

    async def fetch_image(self, ctx, randomize : bool=False, tags : list=[]):
        guild = ctx.message.guild
        search = "https://konachan.com/post.json?limit=1&tags="
        tag_search = "{} ".format(" ".join(tags))
        if randomize:
            tag_search += " order:random"
        search += parse.quote_plus(tag_search)
        message = await ctx.send("Fetching kona image...")
        #try:
        async with aiohttp.get(search) as r:
            website = await r.json()
        if website != []:
            imageURL = "https:{}".format(website[0].get("file_url")).replace(' ', '+')
            return await message.edit('Ok')
        else:
            return await message.edit('Not Ok')
        #except:
        #    await message.delete()
        #    pass

    @commands.command(description='Grabs the last picture from Konachan that matches your keywords.')
    @commands.guild_only()
    async def kona(self, ctx, *tags):
        """Grabs the last picture from Konachan that matches your keywords."""
        try:
            await self.fetch_image(ctx, True, tags)
        except Exception as e:
            await ctx.send("{}, error```py\n{}: {}\n```".format(ctx.message.author.mention, type(e).__name__, str(e)))






def setup(bot):
    cog = Nsfw(bot)
    bot.add_cog(cog)

