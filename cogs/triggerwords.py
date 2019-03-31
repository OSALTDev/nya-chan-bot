import re

from discord import Message
from discord.ext import commands
from types import SimpleNamespace
from .base_cog import BaseCog


class Cog(BaseCog, name="Trigger words"):
    """
    Trigger responses from certain regular expression triggers.
    """
    def __init__(self, bot):
        super().__init__(bot)
        self.triggers = None

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Generates the regex and responses once
        the bot has booted. This information is not
        available until runtime.
        """

        # Add regex here, along with the response the bot should give if it finds a match.
        # We're using {bot} and {user} to refer
        self.triggers = (
            SimpleNamespace(
                regex=re.compile("(:?i'?m|i am) (going|gonna go) to (:?bed|sleep)"),
                response="Good night {user}!"
            ),
            SimpleNamespace(
                regex=re.compile(f"(:?hi|hello|hey there|sup) {self.bot.user.mention}!?"),
                response="Hey {user}!"
            )
        )

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        """
        This event triggers whenever someone sends a message into any channel.

        If the content of the message matches one of our triggers, we'll respond
        with the corresponding message.
        """
        if not self.triggers:
            return

        response = None
        for trigger in self.triggers:
            if trigger.regex.search(message.content):
                response = trigger.response
                break

        if response:
            await message.channel.send(response.format(user=message.author.mention))

    @commands.group(invoke_without_command=True)
    async def trigger(self, ctx):
        await self.no_invoke_help(ctx)

    @trigger.command()
    async def add(self, ctx):
        pass

    @trigger.command()
    async def remove(self, ctx):
        pass

    @trigger.command()
    async def list(self, ctx):
        pass
