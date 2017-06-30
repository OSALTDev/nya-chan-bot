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
        async with aiohttp.ClientSession() as session:
            async with session.get(search) as r:
                website = await r.json()
        if website != []:
            imageId = website[0].get('id')
            embedTitle = "Konachan Image #{}".format(imageId)
            embedLink = "https://konachan.com/post/show/{}".format(imageId)
            rating = website[0].get('rating')
            if rating == "s":
                ratingColor = "00FF00"
                ratingWord = "safe"
            elif rating == "q":
                ratingColor = "FF9900"
                ratingWord = "questionable"
            elif rating == "e":
                ratingColor = "FF0000"
                ratingWord = "explicit"
            tagList = website[0].get('tags').replace(' ', ', ').replace('_', '\_')
            output = discord.Embed(title=embedTitle, url=embedLink, colour=discord.Colour(value=int(ratingColor, 16)))
            output.add_field(name="Rating", value=ratingWord)
            output.add_field(name="Tags", value=tagList, inline=False)
            output.set_thumbnail(url=imageURL)
            await message.edit(content="Requested by {}".format(ctx.message.author.mention), embed=output)

            #imageURL = "https:{}".format(website[0].get("file_url")).replace(' ', '+')
            #await message.edit(content="Requested by {}\n{}".format(ctx.message.author.mention, imageURL))
        else:
            await message.delete()

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

