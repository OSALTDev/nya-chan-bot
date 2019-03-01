#!/usr/bin/env python3
import discord
from discord.ext import commands
from nyalib.NyaBot import NyaBot, ThrowawayException
import sys
import traceback
import re
import os

bot = NyaBot()
arg_regs = (
    {
        "match": re.compile("Member \"(.*)\" not found"),
        "replaced": r"The user **\1** cannot be found"
    },
)


def bad_argument_to_reply_string(err):
    for item in arg_regs:
        if item["match"].match(err.args[0]):
            return item["match"].sub(item["replaced"], err.args[0])
    return err.args[0]


@bot.event
async def on_command_error(ctx, error):
    if error.__class__ not in (commands.CommandNotFound, ThrowawayException):
        msg_list = {
            commands.NotOwner: "Only my Owner can ask me to do that, nya!```{msg.content}```",
            commands.UserInputError: "{msg.author.mention}, Input error```py\n{errn}: {errs}\n```",
            commands.NoPrivateMessage: "{msg.author.mention}, this command cannot be send in a PM!```{msg.content}```",
            commands.CheckFailure: "You don\'t have the permission to use this command, {msg.author.mention}"
                                   "```\n{msg.content}```",
            commands.BadArgument: bad_argument_to_reply_string(error)
        }

        # Get error message by class
        # If error not handled in dict, use general error message
        msg = msg_list.get(error.__class__, "{msg.author}, error```py\n{errn}: {errs}\n```")
        if error.__class__ in (commands.BadArgument, commands.NotOwner, commands.CheckFailure):
            # Only use the reply method if a certain type of error
            # If note one of the set types, then DM
            await ctx.reply(msg.format(msg=ctx.message))
        else:
            await ctx.author.send(msg.format(msg=ctx.message, errn=type(error).__name__, errs=str(error)))
            if os.getenv("DEBUG"):
                raise error


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
    if not os.getenv("DEBUG"):
        return

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
