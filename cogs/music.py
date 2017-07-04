import discord
from discord.ext import commands
from cogs.base_cog import BaseCog

if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')

class Music(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.command(description='Add youtube video to the queue and start playing')
    @commands.guild_only()
    async def play(self, ctx):
        """Play a youtube video"""
        voice_channel = None
        if not ctx.author.voice is None:
            voice_channel = ctx.author.voice.channel
        if not voice_channel is None:
            vc = await voice_channel.connect()
            vc.play(discord.FFmpegPCMAudio('data/music/tmp/CSvFpBOe8eY.m4a'))






def setup(bot):
    cog = Music(bot)
    bot.add_cog(cog)
