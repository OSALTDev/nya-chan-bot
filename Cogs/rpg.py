import random
from discord.ext import commands
import asyncio
import role_ids

class RPG():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Roll some dice ! (Example : 2d6)')
    @commands.guild_only()
    async def roll(self, ctx, dice : str):
        """Roll some dice"""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.channel.send('```{}, format has to be NdN !```'.format(ctx.author.mention))
            return False
        result = [random.randint(1, limit) for r in range(rolls)]
        print(result)
        result = "```Results for {} : {}```".format(dice, ', '.join(str(random.randint(1, limit)) for r in range(rolls)))
        await ctx.channel.send(result)

def setup(bot):
    cog = RPG(bot)
    bot.add_cog(cog)
