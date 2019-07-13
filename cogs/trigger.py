"""
This cog handles chat triggers and responses
"""

# Load config, base cog and commands
from bot.cog_base import Base
from bot.command import command as NyaCommand, commands
from bot.checks import is_moderator, is_admin
from discord import ChannelType as DiscordChannelType, Forbidden as DiscordForbidden

# Import re compile and ignore case, and import simple namespace
from re import compile as re_compile, IGNORECASE as RE_IGNORE_CASE, error as RE_ERROR

from datetime import datetime, timedelta
from asyncio import TimeoutError as AIO_TIMEOUT_ERROR


class setup(Base, name="Trigger"):
    def __init__(self):
        self.db = self.bot.database.collection("TriggerWords")
        self.triggered = self.bot.database.collection("TriggerCount")

        # Initialize cog trigger dictionary and temporary trigger string list
        self.triggers = {}

        guild_re = {}
        for trigger in self.db.entries:
            guild_id = int(trigger['guild'])

            # Add trigger to trigger list, keyed title
            try:
                self.triggers[guild_id][trigger['name']] = trigger
            except KeyError:
                self.triggers[guild_id] = {}
                self.triggers[guild_id][trigger['name']] = trigger

            if guild_id not in guild_re:
                guild_re[guild_id] = []

            guild_re[guild_id].append(trigger['re'])

        # Guild-specific regex
        self.guild_re = {}
        for guild_id, proc_re in guild_re.items():
            self.guild_re[guild_id] = re_compile(r"\b(?:" + "|".join(proc_re) + r")\b", RE_IGNORE_CASE)

    @Base.listener()
    async def on_message(self, message):
        # Don't trigger if bot, or if not in a guild
        if message.author.bot or not message.guild:
            return

        # Get current date and generate the ID with guild and author IDs
        current_date = datetime.now()
        entry_key = str(message.guild.id) + "_" + str(message.author.id)

        # Get entry and, if allowed to trigger, dont return
        entry = self.triggered.entry(entry_key)
        is_allowed = (entry["until"] - current_date.timestamp() <= 0) if entry else True
        if not is_allowed:
            return

        try:
            triggers = self.triggers[message.guild.id]
            re = self.guild_re[message.guild.id]
        except KeyError:
            return

        # Search through entire doc, matches stored in trigger_match
        trigger_match = re.finditer(message.content)

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

        self.triggered.enter({"until": (current_date + timedelta(weeks=2)).timestamp()}, entry_key)

        for name in uniques:
            # Store trigger and do action
            trigger = triggers[name]
            if trigger["action"] == "dm":
                try:
                    await message.author.send(trigger["response"].format(user=message.author))
                except DiscordForbidden:
                    await message.channel.send(trigger["response"].format(user=message.author))
            elif trigger["action"] == "kick":
                try:
                    await message.author.send(trigger["message"])
                    await message.author.kick(reason=f"Triggered kick: {trigger['name']}: {trigger['message']}")
                except:
                    await message.author.kick(reason=f"Triggered kick: {trigger['name']}")
            elif trigger["action"] == "ban":
                try:
                    await message.author.send(trigger["message"])
                    await message.author.ban(reason=f"Triggered ban: {trigger['name']}: {trigger['message']}")
                except:
                    await message.author.ban(reason=f"Triggered ban: {trigger['name']}")

    async def cog_command_error(self, ctx, error):
        # Argument missing
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to specify a trigger name")
        elif isinstance(error.original, AIO_TIMEOUT_ERROR):
            await ctx.send("Command timed out, please try again")

    async def add_dm_trigger(self, ctx):
        def wait_for_message_check(m):
            return m.author.id == ctx.author.id and m.channel.type is DiscordChannelType.private

        await ctx.author.send("What would you like the response to be?")
        action_response = await self.bot.wait_for("message", check=wait_for_message_check, timeout=75)

        return {"response": action_response.content}

    async def add_kick_ban_trigger(self, ctx):
        await ctx.author.send("Please type a reason that I can DM the user, or type '!!' for no message")

        def wait_for_message(m):
            return m.author.id == ctx.author.id and m.channel.type is DiscordChannelType.private

        msg = await self.bot.wait_for("message", check=wait_for_message, timeout=75)

        if msg.content == "!!":
            return {}

        return {"message": msg.content}

    @NyaCommand()
    @is_admin()
    async def add_trigger(self, ctx: commands.Context, trigger_name):
        """
            Add a word trigger to the bot

            Syntax:
                {prefix}add_trigger <trigger_name>
        """
        if self.db.entry(f"{ctx.guild.id}_{trigger_name}"):
            return await ctx.send("This trigger already exists for your guild")

        _reaction_list = {
            # ":mod_message:592400024328077313": ("Message the moderators", "modmsg"),
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
            return u.id == ctx.author.id and m.message.id == user_react_to.id and str(m)[1:-1] in _reaction_list

        reaction, _ = await self.bot.wait_for("reaction_add", check=wait_for_reaction_check, timeout=30)

        await ctx.author.send(
            "Please enter the words you want to trigger on\n"
            "Each word must be sent as a new message\n"
            "Once you have completed the entries, please enter '!!' as a message\n\n"
            "Python regular expressions are allowed to be used as well"
        )

        def wait_for_message_check(m):
            return m.author.id == ctx.author.id and m.channel.type is DiscordChannelType.private

        word_list = []
        user_word = await self.bot.wait_for("message", check=wait_for_message_check, timeout=30)

        while user_word.content != "!!":
            try:
                re_compile(user_word.content)
            except RE_ERROR:
                await user_word.add_reaction("❌")
                continue
            else:
                word_list.append(user_word.content)
                await user_word.add_reaction("✅")
            finally:
                user_word = await self.bot.wait_for("message", check=wait_for_message_check, timeout=30)

        words = "|".join(word_list)
        entry = {
            "guild": str(ctx.guild.id),
            "name": trigger_name,
            "action": _reaction_list[str(reaction)[1:-1]][1],
            "words": word_list,
            "re": f"(?P<{trigger_name}>{words})"
        }

        await user_react_to.delete()

        if entry["action"] == "dm":
            self.db.enter({
                **entry,
                **(await self.add_dm_trigger(ctx))
            }, f"{ctx.guild.id}_{trigger_name}")
        elif entry["action"] in ("kick", "ban"):
            # Ban and kick request the same information
            self.db.enter({
                **entry,
                **(await self.add_kick_ban_trigger(ctx))
            }, f"{ctx.guild.id}_{trigger_name}")

        await ctx.author.send("Your reaction has been inserted")

    @NyaCommand()
    @is_moderator()
    async def list_triggers(self, ctx):
        """
            List your guild's triggers

            Syntax:
                {prefix}list_triggers
        """
        trigger_names = []
        for trigger in self.db.entries:
            if int(trigger["guild"]) == ctx.guild.id:
                trigger_names.append(trigger["name"])

        if not trigger_names:
            await ctx.send("You have no triggers for this guild")
            return

        await ctx.send("Your triggers for this guild are:\n" + ', '.join(trigger_names))

    @NyaCommand()
    @is_admin()
    async def remove_trigger(self, ctx, trigger_name):
        """
            Remove a word trigger from the bot
            
            Syntax:
                {prefix}remove_trigger <trigger_name>
        """
        doc = self.db.entry(f"{ctx.guild.id}_{trigger_name}")
        if doc:
            doc.delete()
            await ctx.send(f"Trigger {trigger_name} successfully deleted")
        else:
            await ctx.send(f"Trigger {trigger_name} does not exist")
