from bot.cog_base import Base
from bot.checks import is_moderator
from bot import command as NyaCommand, commands

import discord
from typing import Union


class setup(Base, name="Self-tagging"):
    def __init__(self):
        self.db = self.bot.database.collection("SelfTagging")

    @NyaCommand.group()
    async def role(self, ctx, *, role: commands.Greedy[discord.Role] = None):
        if role is None:
            await ctx.send("Please tell me what role you want")
            return

        try:
            await ctx.author.add_roles(*role)
        except AttributeError:
            await ctx.message.add_reaction("👎")
        else:
            await ctx.message.add_reaction("👍")

