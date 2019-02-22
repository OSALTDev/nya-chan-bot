import random
from discord.ext import commands
from cogs.base_cog import BaseCog


class RPG(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.command(description='Roll some dice ! (Example : 2d6)')
    @commands.guild_only()
    async def roll(self, ctx, dice: str):
        """Roll some dice"""
        bot_channel = self.bot.get_channel(332644650462478336)
        if bot_channel is None:
            await ctx.channel.send('The dedicated bot commands channel cannot be found')
            return

        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await bot_channel.send('```{}, format has to be NdN !```'.format(ctx.author.mention))
        else:
            result = [random.randint(1, limit) for _ in range(rolls)]
            msg = "```Results for {} : {} (Total : {})```".format(dice, ', '.join(str(x) for x in result), sum(result))
            await bot_channel.send(msg)


def setup(bot):
    cog = RPG(bot)
    bot.add_cog(cog)
