from bot.cog_base import Base, commands
from bot.checks import is_admin, is_owner
from bot import command as NyaCommands
from discord import Role as DiscordRole, utils as DiscordUtils


class setup(Base, name="Permissions"):
    def __init__(self):
        self.db = self.bot.database.collection("ServersJoined")

    def check_has_permission(self, ctx, of):
        guild = self.db.find(guild_id=str(ctx.guild.id))
        if not guild:
            return False

        if f'{of}_role_ids' not in guild.getStore():
            return False

        for role_id in guild[f"{of}_role_ids"]:
            if DiscordUtils.get(ctx.author.roles, id=int(role_id)):
                return True
        return False

    def check_is_admin(self, ctx):
        return self.check_has_permission(ctx, "admin")

    def check_is_moderator(self, ctx):
        return self.check_has_permission(ctx, "mod")

    @NyaCommands.group("config", invoke_without_command=True, protected=True)
    @is_admin()
    async def configure(self, ctx):
        await ctx.send_help(ctx.invoked_with)

    @NyaCommands.command("set_moderators")
    @is_admin()
    async def configure_set_moderator_roles(self, ctx, roles: commands.Greedy[DiscordRole]):
        entry = self.db.find(guild_id=str(ctx.guild.id))
        entry["mod_role_ids"] = [str(role.id) for role in roles]
        entry.save()
        await ctx.message.add_reaction('👍')

    @NyaCommands.command("set_admins")
    @is_owner()
    async def configure_set_admin_roles(self, ctx, roles: commands.Greedy[DiscordRole]):
        entry = self.db.find(guild_id=str(ctx.guild.id))
        entry["admin_role_ids"] = [str(role.id) for role in roles]
        entry.save()
        await ctx.message.add_reaction('👍')

    @Base.listener()
    async def on_ready(self):
        guilds = [guild.id for guild in self.bot.guilds]
        differences = set(guilds) ^ set(int(guild["guild_id"]) for guild in self.db.entries)

        for guild_id in differences:
            if guild_id not in guilds:
                self.db.find(guild_id=str(guild_id)).delete()
            else:
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
        self.db.find(guild_id=str(guild.id)).delete()

    @NyaCommands.command(protected=True)
    async def enable_command(self, ctx, *, command):
        entry = self.db.find(guild_id=str(ctx.guild.id))

        if "disabled_commands" in entry.getStore():
            disabled_commands = entry["disabled_commands"]

            if command in disabled_commands:
                disabled_commands.remove(command)
                entry["disabled_commands"] = disabled_commands

            entry.save()

        await ctx.message.add_reaction('👍')

    @NyaCommands.command(protected=True)
    async def disable_command(self, ctx, *, command):
        entry = self.db.find(guild_id=str(ctx.guild.id))

        if "disabled_commands" not in entry.getStore():
            entry["disabled_commands"] = []

        bot_command: NyaCommands.NyaCommand = self.bot.get_command(command)
        if bot_command.protected:
            await ctx.send("You can't disable this command")
            return

        if command not in entry["disabled_commands"]:
            entry["disabled_commands"].append(command)

        entry.save()
        await ctx.message.add_reaction('👍')
