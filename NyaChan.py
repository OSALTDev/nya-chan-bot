#!/usr/bin/python3
import os
import sys
import psutil
import subprocess
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

loaded_cogs = []

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
    elif isinstance(error, discord.ext.commands.errors.UserInputError):
        await ctx.send("{}, Input error```py\n{}: {}\n```".format(ctx.message.author.mention, type(error).__name__, str(error)))
    elif isinstance(error, discord.ext.commands.errors.NoPrivateMessage):
        await ctx.send("{}, this command cannot be send in a PM!```{}```".format(ctx.message.author.mention, ctx.message.content))
    else:
        await ctx.send("{}, error```py\n{}: {}\n```".format(ctx.message.author.mention, type(error).__name__, str(error)))

@bot.event
async def on_command_completion(ctx):
    await ctx.message.delete()

@bot.command()
@commands.is_owner()
async def load(ctx, cog_name : str):
    """Loads a cog."""
    #try:
    if not cog_name in loaded_cogs:      
        try:  
            bot.load_extension('Cogs.cog_' + cog_name)
            loaded_cogs.append(cog_name)
            await ctx.send("```{} loaded.```".format(cog_name))
        except (AttributeError, ImportError) as e:
            await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            raise commands.UserInputError(ctx)
    else:
        await ctx.send("```py\n'{}' module is already loaded\n```".format(cog_name))
        raise commands.UserInputError(ctx)

@bot.command()
@commands.is_owner()
@commands.guild_only()
async def say(ctx, channel_name : str, *msg):
    """Says something as Nya."""
    channel = None
    for chan in ctx.guild.channels:
        if chan.name == channel_name:
            channel = chan

    if not channel is None:
        await channel.send(" ".join(str(x) for x in msg))
    else:
        await ctx.send("```py\n'{}' channel has not been found\n```".format(channel_name))
        raise commands.UserInputError(ctx, 'Channel not found')
    
@bot.command()
@commands.is_owner()
async def unload(ctx, cog_name : str):
    """Unloads a cog."""
    if cog_name in loaded_cogs:
        bot.unload_extension('Cogs.cog_' + cog_name)
        await ctx.send("```{} unloaded.```".format(cog_name))
        loaded_cogs.remove(cog_name)
    else:
        await ctx.send("```py\n'{}' module is not loaded\n```".format(cog_name))
        raise commands.UserInputError(ctx)

@bot.command()
@commands.is_owner()
async def list_cogs(ctx):
    """List loaded cogs."""
    if len(loaded_cogs) > 0:
        await ctx.send("```Loaded modules : {}```".format(" ".join(str(x) for x in loaded_cogs)))
    else:
        await ctx.send("```No module loaded```")

@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    """Shutdown bot."""
    await bot.logout()


@bot.command()
@commands.is_owner()
async def update(ctx):
    """Update bot."""
    try:
        process = subprocess.check_output("git pull origin master", stderr=subprocess.STDOUT, shell=True)
        print(process)
        await ctx.send("```{" + process + "}```")
    except Exception as e:
        raise commands.UserInputError(ctx) 

@bot.command()
@commands.is_owner()
async def restart(ctx):
    """Restart bot."""
    try:
        p = psutil.Process(os.getpid())
        for handler in p.get_open_files() + p.connections():
            os.close(handler.fd)
    except Exception as e:
        pass
    python = sys.executable
    os.execl(python, python, *sys.argv)

if __name__ == "__main__":
    for cog in startup_cogs:
        try:
            bot.load_extension('Cogs.cog_' + cog)
            loaded_cogs.append(cog)
        except (AttributeError, ImportError) as e:
            pass

bot.run(token)

