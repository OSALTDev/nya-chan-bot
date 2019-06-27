from bot.cog_base import Base
import discord


class setup(Base, name="Moderation"):
    async def kick(self, member: discord.Member, reason):
        pass

    async def ban(self, member: discord.Member, reason, permanent=False):
        pass

