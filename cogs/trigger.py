"""
This cog handles chat triggers and responses
"""

# Load config, base cog and commands
from bot.config import Config
from bot.cog_base import Base
from discord.ext import commands

# Import re compile and ignore case, and import simple namespace
from re import compile as re_compile, IGNORECASE as RE_IGNORE_CASE
from types import SimpleNamespace


class setup(Base, name="Trigger"):
    def __init__(self, bot):
        super().__init__(bot)
        self.db = bot.database.collection("TriggerWords")

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

    @commands.command()
    async def add_trigger(self, ctx: commands.Context, trigger_name, *, trigger_word):
        """
            Add a word trigger to the bot

            Syntax:
                {prefix}add_trigger <trigger_name> <trigger_word>

            You can also use newlines to split words:
                {prefix}add_trigger <trigger_name>
                word1
                word2

            You can use python-style regex in your trigger words
        """
        self.db.enter({
            "words": trigger_word.split("\n")
        }, key=f"{ctx.guild.id}:{trigger_name}")

    @commands.command()
    async def set_trigger_action(self, ctx, trigger_name, trigger_action):
        doc = self.db.entry(f"{ctx.guild.id}:{trigger_name}")
        doc["action"] = trigger_action
        doc.patch()

    @commands.command()
    async def set_trigger_response(self, ctx, trigger_name, *, response):
        doc = self.db.entry(f"{ctx.guild.id}:{trigger_name}")
        doc["response"] = response
        doc.patch()

    @commands.command()
    async def remove_trigger(self, ctx, trigger_name):
        """
            Remove a word trigger from the bot
            
            Syntax:
                {prefix}remove_trigger <trigger_name>
        """
        doc = self.db.entry(f"{ctx.guild.id}:{trigger_name}")
        doc.delete()
