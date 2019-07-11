"""
    This file holds our custom command class
    It adds a bitwise check option to the Discord command class
"""

from discord.ext import commands


class NyaCommand(commands.Command):
    def __init__(self, func, **kwargs):
        super().__init__(func, **kwargs)

        try:
            bitwise_checks = func.__commands_bitwise_checks__
            bitwise_checks.reverse()
            self.bitwise_checks = bitwise_checks
        except AttributeError:
            self.bitwise_checks = []

