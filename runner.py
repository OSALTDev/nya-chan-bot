import bot
import os
import traceback
from discord.ext import commands

BotInstance = bot.BotBase()


# Helper function to load extensions
def _load_and_print_if_error(name):
    try:
        BotInstance.load_extension(name)
    except commands.ExtensionAlreadyLoaded:
        # Ignore error if already loaded
        pass
    except commands.ExtensionError as e:
        # Display error message and log error
        print(f"Failed to load cog: {name}")

        if bot.Config.debug:
            BotInstance.logger.error(traceback.format_exc())
            BotInstance.logger.error(e)


# Populate cogs if cogs dont exist
cogs = bot.BotConfig.cogs
if not cogs:
    cogs = [
        f.replace('.py', '') for f in os.listdir("cogs")
        if os.path.isfile(os.path.join("cogs", f))
        and f.split(".")[-1] == "py"
    ]

# Load all cogs
for cog in cogs:
    _load_and_print_if_error(f"cogs.{cog}")

# Required cogs
_load_and_print_if_error("cogs.core")

# Debug cog
if bot.Config.debug:
    _load_and_print_if_error("jishaku")

# Write PID to a file for stopping with systemctl
pidfile = open(".pid", "w")
pidfile.write(str(os.getpid()))
pidfile.close()

# Begin!
BotInstance.run(bot.BotConfig.token)
