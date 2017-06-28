#!/usr/bin/python3
import sys
import discord
from discord.ext import commands
import role_ids
import configparser

config = configparser.ConfigParser()
config.read_file(open('settings.ini'))

#startup_cogs = ['cog_rpg', 'cog_music', 'cog_misc']

bot = commands.Bot(command_prefix=config['Bot']['prefix'], description=config['Bot']['description'])

if len(sys.argv) == 2 and sys.argv[1] == 'dev':
    token = config['Bot']['token_dev']
else:
    token = config['Bot']['token_prod']

@bot.event
async def on_ready():
    print('######################################################')
    print('#                      Nya Chan                      #')
    print('######################################################')
    print('Discord.py version : ' + discord.__version__)
    print('Bot User : ' + str(bot.user))
    app_infos = await bot.application_info()
    bot.owner_id = app_infos.owner.id
    print('Bot Owner : ' + str(bot.owner_id))
    url = discord.utils.oauth_url(app_infos.id)
    print('Oauth URL : ' + str(url))

@bot.event
async def on_message(message):
    if not message.content.startswith(config['Bot']['prefix']):
        return False
    if message.author.bot:
        return False
    await bot.process_commands(message)


@bot.command()
async def load(cog_name : str):
    """Loads a cog."""
    try:
        bot.load_extension(cog_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("{} loaded.".format(cog_name))

if __name__ == "__main__":
    for cog in startup_cogs:
        bot.load_extension(cog)

bot.run(token)

