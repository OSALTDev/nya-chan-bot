import discord
from discord.ext import commands
import asyncio
import role_ids

if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')

class Music():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Add youtube video to the queue and start playing')
    @commands.guild_only()
    async def play(self, ctx):
        """Play a youtube video"""
        voice_channel = None
        if not ctx.author.VoiceState is None:
            print('not in voice')
        else:
            print('in voice channel : {}'.format(ctx.author.VoiceState.channel.name))
            






def setup(bot):
    cog = Music(bot)
    bot.add_cog(cog)
