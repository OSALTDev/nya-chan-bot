from bot import BotBase
from discord.ext import commands


class BaseMeta(commands.CogMeta):
    def __new__(mcs, *args, **kwargs):
        name, bases, attrs = args
        new_cls = super().__new__(mcs, name, bases, attrs, **kwargs)
        # noinspection PyTypeChecker
        new_cls.bot: BotBase = None
        return new_cls

    def __init__(cls, *args, **kwargs):
        def custom_init(self, bot=None):
            if bot:
                cls.bot = bot
                cls.__cog__init__(self)
                bot.add_cog(self)

        cls.__cog__init__ = cls.__init__
        cls.__init__ = custom_init
        super().__init__(*args)


class Base(commands.Cog, metaclass=BaseMeta):
    pass
