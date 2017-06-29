import random
from discord.ext import commands
import asyncio
import role_ids

def in_list(list, filter):
    for x in list:
        if filter(x):
            return True
    return False

class RPG():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, description='Roll some dice ! (Example : 2d6)')
    @asyncio.coroutine
    def roll(self, ctx, dice : str):
        if not in_list(ctx.message.author.roles, lambda x: x.name in ['@everyone']):
            yield from bot.send_message(ctx.message.channel, 'You do not have the permission to do that !')
            return False
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            yield from self.bot.say('Format has to be NdN !')
            return False
        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        yield from self.bot.say(result)

def setup(bot):
    bot.add_cog(RPG(bot))
