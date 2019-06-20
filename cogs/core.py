"""
Cog for base events (such as logging, etc)
"""

import logging
import traceback

from bot.cog_base import Base, commands
from bot.config import Bot as BotConfig, Logging


class setup(Base, name="Core"):
    def __init__(self, bot):
        super().__init__(bot)

        self.command_log = self._create_logger_for("commands")

    def _create_logger_for(self, logger_name):
        logger = logging.getLogger(f'nya.{logger_name}')

        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(filename=f'logs/nya.{logger_name}.log', encoding='utf-8', mode='w')

        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        logger.addHandler(handler)

        return logger

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context):
        if BotConfig.debug and Logging.Command.execute:
            self.command_log.info(f"User {ctx.author} executing command {ctx.invoked_with}")

    @commands.Cog.listener()
    async def on_command_error(self, _, error):
        if BotConfig.debug and Logging.Command.error:
            self.command_log.debug(f"Above command gave error")
            formatted_exception = traceback.format_exception(type(error), error, None)
            self.command_log.error('\n' + "".join(formatted_exception).strip())

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        if BotConfig.debug and Logging.Command.complete:
            self.command_log.info(f"Command complete")
