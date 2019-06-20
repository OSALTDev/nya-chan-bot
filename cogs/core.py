"""
Cog for base events (such as logging, etc)

Events are only logged if debug is on, or if the
specific event is enabled in the config.yaml
"""

# Comprehensive error and logging
import logging
import traceback

# Import cog base and re-use commands; import our config too
from bot.cog_base import Base, commands
from bot.config import Config, Logging


class setup(Base, name="Core"):
    def __init__(self, bot):
        super().__init__(bot)

        # Create event loggers
        self.command_log = self._create_logger_for("commands")
        self.chat_log = self._create_logger_for("chat")

    # Helper function to create logger instances
    @staticmethod
    def _create_logger_for(logger_name):
        logger = logging.getLogger(f'nya.{logger_name}')

        logger.setLevel(logging.DEBUG if Config.debug else logging.INFO)
        handler = logging.FileHandler(filename=f'logs/nya.{logger_name}.log', encoding='utf-8', mode='w')

        # time:LEVEL:logname: message
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        logger.addHandler(handler)

        return logger

    # Log commands being executed
    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context):
        if Logging.Command.execute:
            self.command_log.info(f"User {ctx.author} executing command {ctx.invoked_with}")

    # Log command errors
    @commands.Cog.listener()
    async def on_command_error(self, _, error):
        if Logging.Command.error:
            # Get exception info, in a list
            formatted_exception = traceback.format_exception(type(error), error, None)
            self.command_log.error(
                f"Above command gave error\n" + "".join(formatted_exception).strip()
            )

    # Log command completions
    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        if Logging.Command.complete:
            self.command_log.info(f"Command complete")

    @commands.Cog.listener()
    async def on_message(self, message):
        if Logging.chat:
            self.chat_log.info(f"{message.guild} @ #{message.channel} : @{message.author} : {message.content}")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if Logging.chat:
            self.chat_log.info(
                f"Message {before.guild} @ #{before.channel} : @{before.author} edited\n"
                f"Before:\n{before.content}\n"
                f"After:\n{after.content}"
            )
