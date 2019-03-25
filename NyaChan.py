#!/usr/bin/env python3
import discord
from discord.ext import commands
from nyalib.NyaBot import NyaBot, ThrowawayException
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
            commands.CheckFailure: "You don\'t have the permission to use this command"
                                   "```\n{msg.content}```",
            commands.BadArgument: bad_argument_to_reply_string(error)
        }

        # Get error message by class
        # If error not handled in dict, use general error message
        msg = msg_list.get(error.__class__, "{msg.author}, error```py\n{errn}: {errs}\n```")
        msg = msg.format(msg=ctx.message, err=error, errn=type(error).__name__, errs=str(error))
        if error.__class__ not in (commands.UserInputError, commands.NoPrivateMessage):
            await ctx.reply.dm(msg)
            if os.getenv("DEBUG"):
                raise error
        else:
            # Only use the reply method if a certain type of error
            # If note one of the set types, then DM
            await ctx.reply(msg)


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
async def on_error(*args):
    if not os.getenv("DEBUG"):
        return

    raise next(t for t in args if isinstance(t, Exception))


class MainDriver:
    def __init__(self, bot):
        self.bot = bot
        for cog in self.bot.config.bot.cogs:
            try:
                self.bot.load_extension(('cogs.' if cog["in_cogs"] else "") + cog["file"])
            except (commands.ExtensionFailed, commands.ExtensionError, commands.ExtensionNotFound) as e:
                print(f"Failed to load cog: {cog['file']} due to {e}")

    def run(self):
        token = self.bot.config.bot.token
        self.bot.run(token)


if __name__ == "__main__":
    m = MainDriver(bot)
    m.run()
