"""
This cog handles chat triggers and responses
"""

# Load config, base cog and commands
from bot.config import Config
from bot.cog_base import Base
from discord.ext import commands

# Import re compile and ignore case, and import simple namespace
from re import compile as re_compile, IGNORECASE as RE_IGNORE_CASE, error as RE_ERROR
from types import SimpleNamespace

from asyncio import TimeoutError as AIO_TIMEOUT_ERROR


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

    async def cog_command_error(self, ctx, error):
        if isinstance(error.original, AIO_TIMEOUT_ERROR):
            await ctx.send("Command timed out, please try again")

    async def add_dm_trigger(self, ctx):
        await ctx.author.send(
            "Please enter the words you want to trigger on\n"
            "Each word must be sent as a new message\n"
            "Once you have completed the entries, please enter '!!' as a message\n\n"
            "Python regular expressions are allowed to be used as well"
        )

        def wait_for_message_check(m):
            return m.author.id == ctx.author.id and not m.guild

        word_list = []
        user_word = await self.bot.wait_for("message", check=wait_for_message_check, timeout=30)

        while user_word.content != "!!":
            try:
                re_compile(user_word.content)
            except RE_ERROR:
                continue
            else:
                word_list.append(user_word.content)
            finally:
                user_word = await self.bot.wait_for("message", check=wait_for_message_check)

        await ctx.author.send("What would you like the response to be?")
        action_response = await self.bot.wait_for("message", check=wait_for_message_check, timeout=75)

        return {"words": word_list, "response": action_response}

    @commands.command()
    @commands.guild_only()
    async def add_trigger(self, ctx: commands.Context, trigger_name):
        """
            Add a word trigger to the bot

            Syntax:
                {prefix}add_trigger <trigger_name>
        """
        if self.db.entry(f"{ctx.guild.id}_{trigger_name}"):
            return await ctx.send("This trigger already exists for your guild")

        _reaction_list = {
            ":mod_message:592400024328077313": ("Message the moderators", "modmsg"),
            ":dm_user:592400024520884246": ("DM the user", "dm"),
            ":kick_user:592400025548750858": ("Kick user", "kick"),
            ":ban_user:592400024605032474": ("Ban user", "ban")
        }

        user_react_to = await ctx.author.send(
            "React with the action of your trigger:\n" +
            "\n".join(f"<{reaction}> - {reaction_desc[0]}" for reaction, reaction_desc in _reaction_list.items())
        )

        for reaction in _reaction_list.keys():
            await user_react_to.add_reaction(reaction)

        def wait_for_reaction_check(m, u):
            return u.id == ctx.author.id and m.message.id == user_react_to.id

        reaction, _ = await self.bot.wait_for("reaction_add", check=wait_for_reaction_check, timeout=30)

        entry = {
            "name": trigger_name,
            "action": _reaction_list[str(reaction)[1:-1]][1]
        }

        await user_react_to.delete()

        if entry["action"] == "dm":
            self.db.enter({
                **entry,
                **(await self.add_dm_trigger(ctx))
            }, f"{ctx.guild.id}_{trigger_name}")

        await ctx.author.send("Your reaction has been inserted")

    @commands.command()
    async def remove_trigger(self, ctx, trigger_name):
        """
            Remove a word trigger from the bot
            
            Syntax:
                {prefix}remove_trigger <trigger_name>
        """
        doc = self.db.entry(f"{ctx.guild.id}:{trigger_name}")
        doc.delete()
