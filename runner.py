import bot
from discord.ext import commands

BotInstance = bot.BotBase()

for cog in bot.BotConfig.cogs:
    try:
        BotInstance.load_extension(cog)
    except commands.ExtensionError as e:
        print(f"Failed to load cog: {cog['file']} due to {e}")

BotInstance.run(bot.BotConfig.token)
