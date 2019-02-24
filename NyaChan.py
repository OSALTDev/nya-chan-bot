#!/usr/bin/env python3
import discord
from discord.ext import commands
from nyalib.NyaBot import NyaBot, ThrowawayException
import sys
import traceback
import re
import os

bot = NyaBot()


@bot.event
async def on_command_error(ctx, error):
    if not isinstance(error, ThrowawayException):
        msg_list = {
            commands.CommandNotFound: "{msg.author.mention}, this command does not exist!```{msg.content}```",
            commands.NotOwner: "{msg.author.mention}, only my Owner can ask me to do that, nya!```{msg.content}```",
            commands.UserInputError: "{msg.author.mention}, Input error```py\n{errn}: {errs}\n```",
            commands.NoPrivateMessage: "{msg.author.mention}, this command cannot be send in a PM!```{msg.content}```",
            commands.CheckFailure: "You don\'t have the permission to use this command, {msg.author.mention}"
                                   "```\n{msg.content}```"
        }

        # Get error message by class
        # If error not handled in dict, use general error message
        msg = msg_list.get(error.__class__, "{msg.author}, error```py\n{errn}: {errs}\n```")
        print("\"" + msg + "\"")
        await ctx.author.send(msg.format(msg=ctx.message, errn=type(error).__name__, errs=str(error)))


@bot.event
async def on_command_completion(ctx):
    # Deletes message if no mentions
    if not ctx.message.mentions:
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            # Can't execute on DM channel
            pass


@bot.event
async def on_error(_, msg):
    cls, exc, tb = sys.exc_info()

    if cls == ThrowawayException:
        return

    await msg.add_reaction("🚫")
    err_str = str(cls) + ": " + str(exc.args[1]) + "\n\nTraceback:\n"
    ttb = []

    sep = "\\" if os.name == "nt" else "/"
    for ln in traceback.format_tb(tb, 50):
        ln_m = re.match("  File \"(.*)\", line (\d+), in ([^\s]+)\n(.*)", ln, re.DOTALL)

        p = ln_m.group(1).split(sep)
        lnn = ln_m.group(2)

        tp = []
        for i in p:
            if not tp:
                if i != "site-packages":
                    continue
                i = "<pip_pkg>"
            tp.append(i)

        ttb.append("  {} : {} ({})\n{} {}".format(
            sep.join(tp or p), lnn, ln_m.group(3), " " if tp else ">", ln_m.group(4)))

    err_str += "".join(ttb)
    print(err_str)


class MainDriver:
    def __init__(self, bot):
        self.bot = bot
        for cog in self.bot.config.bot.cogs:
            try:
                self.bot.load_extension('cogs.' + cog)
            except (AttributeError, ImportError) as e:
                print("Failed to load cog: {} due to {}".format(cog, str(e)))

    def run(self):
        token = self.bot.config.bot.token
        self.bot.run(token)


if __name__ == "__main__":
    m = MainDriver(bot)
    m.run()
