#!/usr/bin/env python3
import discord
from discord.ext import commands
from nyalib.NyaBot import NyaBot

bot = NyaBot()


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
        await ctx.author.send(
            "{}, this command does not exist!```{}```".format(ctx.message.author.mention, ctx.message.content))
    elif isinstance(error, discord.ext.commands.errors.NotOwner):
        await ctx.author.send("{}, only my Owner can ask me to do that, nya!```{}```".format(ctx.message.author.mention,
                                                                                             ctx.message.content))
    elif isinstance(error, discord.ext.commands.errors.UserInputError):
        await ctx.author.send(
            "{}, Input error```py\n{}: {}\n```".format(ctx.message.author.mention, type(error).__name__, str(error)))
    elif isinstance(error, discord.ext.commands.errors.NoPrivateMessage):
        await ctx.author.send(
            "{}, this command cannot be send in a PM!```{}```".format(ctx.message.author.mention, ctx.message.content))
    elif isinstance(error, discord.ext.commands.errors.CheckFailure):
        await ctx.author.send(
            "You don\'t have the permission to use this command, {}```{}```".format(ctx.message.author.mention,
                                                                                    ctx.message.content))
    else:
        await ctx.author.send(
            "{}, error```py\n{}: {}\n```".format(ctx.message.author.mention, type(error).__name__, str(error)))
    has_mention = False
    for arg in ctx.args:
        if '@' in str(arg):
            has_mention = True
            break
    if has_mention is True:
        return False
    await ctx.message.delete()


@bot.event
async def on_command_completion(ctx):
    has_mention = False
    for arg in ctx.args:
        if '@' in str(arg):
            has_mention = True
            break
    if has_mention is True:
        return False
    await ctx.message.delete()


class MainDriver:
    def __init__(self, bot):
        self.bot = bot
        for cog in self.bot.config.bot.cogs:
            self.bot.load_cog(cog)

    def run(self):
        token = self.bot.config.bot.token
        self.bot.run(token)


if __name__ == "__main__":
    m = MainDriver(bot)
    m.run()
