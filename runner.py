import bot
import os
import traceback
import logging
from discord.ext import commands

BotInstance = bot.BotBase()


def _load_and_print_if_error(name):
    try:
        BotInstance.load_extension(name)
    except commands.ExtensionAlreadyLoaded:
        pass
    except commands.ExtensionError as e:
        print(f"Failed to load cog: {name}")

        if bot.BotConfig.debug:
            logger = logging.getLogger('nya')
            logger.setLevel(logging.DEBUG)
            handler = logging.FileHandler(filename='nya-debug.log', encoding='utf-8', mode='w')
            handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
            logger.addHandler(handler)

            logger.error(traceback.format_exc())
            logger.error(e)


cogs = bot.BotConfig.cogs
if not cogs:
    cogs = [
        f.replace('.py', '') for f in os.listdir("cogs")
        if os.path.isfile(os.path.join("cogs", f))
        and f.split(".")[-1] == "py"
    ]

for cog in cogs:
    _load_and_print_if_error(f"cogs.{cog}")

# Required cogs
_load_and_print_if_error("cogs.core")
_load_and_print_if_error("jishaku")

BotInstance.run(bot.BotConfig.token)
