"""
    This file holds our custom command class
    It adds a bitwise check option to the Discord command class
"""

from discord.ext import commands
from .checks import CHECK_FAIL


class NyaCommand(commands.Command):
    def __init__(self, func, **kwargs):
        super().__init__(func, **kwargs)

        try:
            bitwise_checks = func.__commands_bitwise_checks__
            bitwise_checks.reverse()
            self.bitwise_checks = bitwise_checks
        except AttributeError:
            self.bitwise_checks = []

    async def can_run(self, ctx):
        if not await super().can_run(ctx):
            return False

        if ctx.command.name == "help":
            return True

        for f in ctx.command.bitwise_checks:
            if f(ctx) & CHECK_FAIL:
                return False

        return True


class NyaGroup(commands.Group, NyaCommand):
    def command(self, *args, **kwargs):
        def decorator(func):
            kwargs.setdefault('parent', self)
            result = command(*args, **kwargs)(func)
            self.add_command(result)
            return result

        return decorator

    def group(self, *args, **kwargs):
        def decorator(func):
            kwargs.setdefault('parent', self)
            result = group(*args, **kwargs)(func)
            self.add_command(result)
            return result

        return decorator


def command(*args, **kwargs):
    kwargs.update(cls=NyaCommand)
    return commands.command(*args, **kwargs)


def group(*args, **kwargs):
    kwargs.update(cls=NyaGroup)
    return commands.group(*args, **kwargs)

