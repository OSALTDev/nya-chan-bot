import random
from discord.ext import commands
from cogs.base_cog import BaseCog


class RPG(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)

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
        msg = "```Results for {} : {} (Total : {})```".format(dice, ', '.join(str(x) for x in result), sum(result))
        await ctx.channel.send(msg)

def setup(bot):
    cog = RPG(bot)
    bot.add_cog(cog)
