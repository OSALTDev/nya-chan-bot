from bot.cog_base import Base, commands
from discord import Role as DiscordRole


class setup(Base, name="Permissions"):
    def __init__(self):
        self.db = self.bot.database.collection("ServersJoined")
        self.unconfigured = []

    async def execution_allowed(self, ctx):
        if isinstance(ctx.command.cog, setup) or ctx.command.name == "help":
            return True

        if ctx.guild.id in self.unconfigured:
            return False

        return True

    @commands.group("config", invoke_without_command=True)
    async def configure(self, ctx):
        pass

    @configure.command("set_moderators")
    async def configure_set_moderator_roles(self, ctx, roles: commands.Greedy[DiscordRole]):
        entry = self.db.find(id=str(ctx.guild.id))
        entry["mod_role_ids"] = [str(role.id) for role in roles]
        entry["configured"] = True
        entry.save()

    @configure.command("set_admins")
    async def configure_set_admin_roles(self, ctx, roles: commands.Greedy[DiscordRole]):
        entry = self.db.find(id=str(ctx.guild.id))
        entry["admin_role_ids"] = [str(role.id) for role in roles]
        entry["configured"] = True
        entry.save()

    @configure.command("prefix")
    async def configure_prefix(self, ctx, *, prefix):
        entry = self.db.find(id=str(ctx.guild.id))
        entry["prefix"] = prefix
        entry.save()

    @Base.listener()
    async def on_ready(self):
        guilds = [guild.id for guild in self.bot.guilds]
        differences = set(guilds) ^ set(int(guild["guild_id"]) for guild in self.db.entries)
        for guild_id in differences:
            if guild_id not in guilds:
                self.db.find(id=str(guild_id)).delete()
            else:
                self.unconfigured.append(guild_id)
                self.db.enter(
                    dict(
                        guild_id=str(guild_id)
                    )
                )

    @Base.listener()
    async def on_guild_join(self, guild):
        self.db.enter(
            dict(
                guild_id=str(guild.id)
            )
        )

    @Base.listener()
    async def on_guild_remove(self, guild):
        self.db.find(id=str(guild.id)).delete()

