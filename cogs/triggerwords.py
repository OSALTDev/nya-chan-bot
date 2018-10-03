import re

from discord import Message
from discord.ext.commands import Bot


# Add regex here, along with the response the bot should give if it finds a match.
# We're using {bot} and {user} to refer
RESPONSES = {
    r"(:?i'?m|i am) (going|gonna go) to (:?bed|sleep)": "Good night {user}!",
    r"(:?hi|hello|hey there|sup) {bot}!?": "Hey {user}!",
}


class TriggerWords:
    """
    Trigger responses from certain regular expression triggers.
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    async def on_ready(self):
        """
        Replaces {bot} with the bot mention after
        the bot has booted. This information is not
        available until runtime.
        """

        keys = list(RESPONSES.keys())

        for key in keys:
            changed_key = key.replace("{bot}", self.bot.user.mention)

            if key != changed_key:
                RESPONSES[changed_key] = RESPONSES[key]
                del RESPONSES[key]

    async def on_message(self, message: Message):
        """
        This event triggers whenever someone sends a message into any channel.

        If the content of the message matches one of our triggers, we'll respond
        with the corresponding message.
        """

        content = message.content

        response = None
        for trigger in RESPONSES.keys():
            if re.search(trigger, content):
                response = RESPONSES.get(trigger)

        if response:
            await message.channel.send(response.format(user=message.author.mention))


def setup(bot):
    bot.add_cog(TriggerWords(bot))
