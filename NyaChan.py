#!/usr/bin/python3
import sys
import discord
from discord.ext import commands
import configparser

config = configparser.ConfigParser()
config.read_file(open('settings.ini'))

startup_cogs = ['welcome']

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
    if message.author.bot:
        return False
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("{}, this command does not exist!```{}```".format(ctx.message.author.mention, ctx.message.content))
    elif isinstance(error, discord.ext.commands.errors.NotOwner):
        await ctx.send("{}, only my Master can ask me to do that, nya!```{}```".format(ctx.message.author.mention, ctx.message.content))

@bot.event
async def on_command_completion(ctx):
    await ctx.message.delete()

@bot.command()
@commands.is_owner()
async def load(ctx, cog_name : str):
    """Loads a cog."""
    #try:
    bot.load_extension('Cogs.' + cog_name)
    #except (AttributeError, ImportError) as e:
    #    print(type(e).__name__)
    #    print(str(e))
    #    await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
    #    return
    #await ctx.send("{} loaded.".format(cog_name))

@bot.command()
@commands.is_owner()
async def unload(ctx, cog_name : str):
    """Unloads a cog."""
    bot.unload_extension('Cogs.' + cog_name)
    await ctx.send("{} unloaded.".format(cog_name))

if __name__ == "__main__":
    for cog in startup_cogs:
        bot.load_extension('Cogs.cog_' + cog)

bot.run(token)

