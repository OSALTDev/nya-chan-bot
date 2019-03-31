import random
from discord.ext import commands
from cogs.base_cog import BaseCog


class Cog(BaseCog, name="RPG"):
    @commands.command(description='Roll some dice ! (Example : 2d6)')
    @commands.guild_only()
    async def roll(self, ctx, dice: str):
        """Roll some dice"""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.reply(f'```{ctx.author.mention}, format has to be NdN !```')
        else:
            result = [random.randint(1, limit) for _ in range(rolls)]
            msg = "```Results for {} : {} (Total : {})```".format(dice, ', '.join(str(x) for x in result), sum(result))
            await ctx.reply(msg)


def setup(bot):
    cog = RPG(bot)
    bot.add_cog(cog)
