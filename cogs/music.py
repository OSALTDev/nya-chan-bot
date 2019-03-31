import discord
from discord.ext import commands
from cogs.base_cog import BaseCog

if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')


class Cog(BaseCog, name="Music"):
    @commands.command(description='Add youtube video to the queue and start playing')
    @commands.guild_only()
    async def play(self, ctx):
        """Play a youtube video"""
        voice_channel = None
        if ctx.author.voice is not None:
            voice_channel = ctx.author.voice.channel
        if voice_channel is not None:
            vc = await voice_channel.connect()
            vc.play(discord.FFmpegPCMAudio('data/music/tmp/CSvFpBOe8eY.m4a'))
