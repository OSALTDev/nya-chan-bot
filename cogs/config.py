import discord
from discord.ext import commands
from .base_cog import BaseCog


class Cog(BaseCog, name="Configuration"):
    @commands.Cog.listener()
    async def on_ready(self):
        pass

    @commands.group()
    async def config(self, ctx):
        pass

    @config.group()
    async def set(self, ctx):
        pass

    @config.group()
    async def view(self, ctx):
        pass
