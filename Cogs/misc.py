from discord.ext import commands
import asyncio
import datetime
import role_ids

def in_list(list, filter):
    for x in list:
        if filter(x):
            return True
    return False

class Misc():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, description='Reward Nya with a gentle pat.')
    @asyncio.coroutine
    def pat(self, ctx, location : str = 'head'):
        if not in_list(ctx.message.author.roles, lambda x: x.name in ['@everyone']):
            yield from bot.send_message(ctx.message.channel, 'You do not have the permission to do that !')
            return False
        if location in ['head']:
            msg = 'Nyaaaaaah, Thank you {} =^.^='.format(ctx.message.author.display_name)
        else:
            msg = 'Eeeeeeeeeeek !!'
        yield from self.bot.say(msg)

    @commands.command(pass_context=True, description='Get the number of minutes to wait until Nixie\'s next steam.')
    @asyncio.coroutine
    def stream(self, ctx):
        if not in_list(ctx.message.author.roles, lambda x: x.name in ['@everyone']):
            yield from bot.send_message(ctx.message.channel, 'You do not have the permission to do that !')
            return False
        now = datetime.datetime.now()
        launch = datetime.datetime(2017, 6, 27, 22, 0, 0, 0)
        delta = launch - now
        minutes = round(delta.days * 24 * 60 + delta.seconds / 60 + delta.microseconds / 60000000)
        yield from self.bot.say("{} minutes until Nixie's next stream, YAY !".format(minutes))

    @commands.command(pass_context=True, description='Explain how to get into the Patreons group.')
    @asyncio.coroutine
    def patreon(self, ctx):
        if not in_list(ctx.message.author.roles, lambda x: x.name in ['@everyone']):
            yield from bot.send_message(ctx.message.channel, 'You do not have the permission to do that !')
            return False
        msg = '''```To all the lovely people here supporting Nixie on patreon who are not in the Patreons group here on discord, please follow these steps.
- Log in to your patreon.
- Head to your account settings.
- Make sure you have linked your discord account to patreon.
- Head to "your pledges"
- Edit your Nixie's pledge, and click update (you don't have to change it)
- You should end up on the thank you page where a button to join the discord server is located.
- Click on it ! ```'''
        yield from self.bot.say(msg)

def setup(bot):
    bot.add_cog(Misc(bot))

