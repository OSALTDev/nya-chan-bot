"""
This cog handles chat triggers and responses
"""

# Load config and base cog
from bot.config import Config
from bot.cog_base import Base

# Import re compile and ignore case, and import simple namespace
from re import compile as re_compile, IGNORECASE as RE_IGNORE_CASE
from types import SimpleNamespace


class setup(Base, name="Trigger"):
    def __init__(self, bot):
        super().__init__(bot)

        # Initialize cog trigger dictionary and temporary trigger string list
        self.triggers = {}
        trigger_list = []

        for trigger in Config.triggers:
            # Dict => SimpleNamespace
            trigger = SimpleNamespace(**trigger)

            # Store title and joined word list
            title = trigger.title
            words = "|".join(trigger.wordlist)

            # Add trigger to word list
            trigger_list.append(f"(?P<{title}>{words})")

            # Add trigger to trigger list, keyed title
            self.triggers[title] = trigger

        # Compile batch RE
        self.re = re_compile("|".join(trigger_list), RE_IGNORE_CASE)

    @Base.listener()
    async def on_message(self, message):
        # Don't trigger if bot
        if message.author.bot:
            return

        # Search through entire doc, matches stored in trigger_match
        trigger_match = self.re.finditer(message.content)

        # Don't continue if no match
        if not trigger_match:
            return

        # Unique match names
        uniques = []

        # Loop over matches, add unique names to unique list
        for trigger in trigger_match:
            groups = trigger.groupdict()
            for name in groups.keys():
                if groups[name] and name not in uniques:
                    uniques.append(name)

        for name in uniques:
            # Store trigger and do action
            trigger = self.triggers[name]
            if trigger.action == "dm":
                await message.author.send(trigger.response)
