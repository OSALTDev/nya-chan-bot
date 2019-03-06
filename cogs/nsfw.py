from discord.ext import commands
from urllib import parse
import aiohttp

from cogs.base_cog import BaseCog


class Cog(BaseCog, name="NSFW"):
    """Gives functions for the pervs out there ;-)"""
    async def fetch_image(self, ctx, channel, randomize=False, tags=[]):
        search = "https://konachan.com/post.json?limit=1&tags="
        tag_search = "{} ".format(" ".join(tags))
        if randomize:
            tag_search += " order:random"

        search += parse.quote_plus(tag_search)
        message = await channel.send("Fetching kona image...")

        async with aiohttp.ClientSession() as session:
            async with session.get(search) as r:
                website = await r.json()

        if not website:
            await message.delete()
            return

        image_url = "https:{}".format(website[0].get("file_url")).replace(' ', '+')
        await message.edit(content="Requested by {}\n{}".format(ctx.message.author.mention, image_url))

    @commands.command(description='Grabs a random picture from Konachan that matches your keywords.')
    @commands.guild_only()
    async def kona(self, ctx, *, tags):
        """Grabs a random picture from Konachan that matches your keywords."""
        channel = self.bot.get_channel(self.config.bot.channel.nsfw)
        if channel is not None:
            try:
                await self.fetch_image(ctx, channel, True, tags)
            except Exception as e:
                await ctx.send(
                    "{}, error```py\n{}: {}\n```".format(ctx.message.author.mention, type(e).__name__, str(e)))
