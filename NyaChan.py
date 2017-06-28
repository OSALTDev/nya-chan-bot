import discord
from discord.ext import commands
import asyncio
import role_ids
import configparser

config = configparser.ConfigParser()
config.read_file(open('settings.ini'))


command_prefix='!n.'
startup_cogs = ['cog_rpg', 'cog_music', 'cog_misc']

bot = commands.Bot(command_prefix=config['Bot']['prefix'], description=config['Bot']['description'])

@bot.event
@asyncio.coroutine
def on_ready():
    print('######################################################')
    print('#                      Nya Chan                      #')
    print('######################################################')
    print('Bot User : ' + str(bot.user))
    url = yield from get_oauth_url()
    print('Oauth URL : ' + str(url))

@asyncio.coroutine
def get_oauth_url():
    data = yield from bot.application_info()
    return discord.utils.oauth_url(data.id)

def in_list(list, filter):
    for x in list:
        if filter(x):
            return True
    return False

def welcome_message():
    text = '''Hello there, {0.mention} ! Welcome to **{1.name}** - our rebooted community of geeks and those who love them.

No hate speech allowed. Being a geek transcends language barriers, cultural differences and political climates - so come join the conversation and geek out with us!

:small_blue_diamond: Have a question for Nixie? Check out the <#325268652897075210> channel, where you can ask them, or upvote existing ones, and she will answer them on stream. 
:small_blue_diamond: Propose your ideas for our geek community in <#328703168789610497>!

**News:**
The live stream will be on Tuesday @ 1PM PDT
http://surprise.nixiepixel.com/'''
    return text

@bot.event
@asyncio.coroutine
def on_message(message):
    if not message.content.startswith(command_prefix):
        return False
    if message.author.bot:
        return False
    yield from bot.process_commands(message)

@bot.event
@asyncio.coroutine
def on_member_join(member):
    server = member.server
    text = welcome_message()
    try:
        yield from bot.send_message(member, text.format(member, server))
    except:
        pass

@bot.command(pass_context=True, description='Get a PM with the welcome message.')
@asyncio.coroutine
def welcome(ctx):
    if not in_list(ctx.message.author.roles, lambda x: x.id == '325197025719091201'):
        yield from bot.send_message(ctx.message.channel, 'You do not have the permission to do that !')
        return False
    server = ctx.message.server
    text = welcome_message()
    yield from bot.send_message(ctx.message.author, text.format(ctx.message.author, server))

@bot.command(pass_context=True, hidden=True)
@asyncio.coroutine
def nowplaying(ctx, game_name : str):
    if not in_list(ctx.message.author.roles, lambda x: x.name in ['Master Control', 'Nixie']):
        yield from bot.send_message(ctx.message.channel, 'You do not have the permission to do that !')
        return False
    yield from bot.change_presence(game=discord.Game(name=game_name))

@bot.command(pass_context=True, hidden=True)
@asyncio.coroutine
def shutdown(ctx):
    if not in_list(ctx.message.author.roles, lambda x: x.name in ['Master Control', 'Nixie']):
        yield from bot.send_message(ctx.message.channel, 'You do not have the permission to do that !')
        return False
    yield from bot.logout()

@bot.command(pass_context=True, hidden=True)
@asyncio.coroutine
def role_ids(ctx):
    if not in_list(ctx.message.author.roles, lambda x: x.name in ['Master Control']):
        yield from bot.send_message(ctx.message.channel, 'You do not have the permission to do that !')
        return False
    for role in ctx.message.server.roles:
        print('{} - {}'.format(role.name, role.id))

if __name__ == "__main__":
    for cog in startup_cogs:
        bot.load_extension(cog)

bot.run(token)

