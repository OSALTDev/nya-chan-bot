from bot.config import Config
from bot.cog_base import Base
from re import compile as re_compile, IGNORECASE as RE_IGNORE_CASE
from types import SimpleNamespace


class setup(Base, name="Trigger"):
    def __init__(self, bot):
        super().__init__(bot)

        self.triggers = {}
        word_list = []

        for trigger in Config.triggers:
            trigger = SimpleNamespace(**trigger)
            title = trigger.title
            words = "|".join(trigger.wordlist)

            word_list.append(f"(?P<{title}>{words})")
            self.triggers[title] = trigger

        self.re = re_compile("|".join(word_list), RE_IGNORE_CASE)

    @Base.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        trigger_match = self.re.search(message.content)
        if trigger_match:
            triggers = trigger_match.groupdict()
            for name, value in triggers.items():
                if not value:
                    continue

                trigger = self.triggers[name]
                if trigger.action == "dm":
                    await message.author.send(trigger.response)
