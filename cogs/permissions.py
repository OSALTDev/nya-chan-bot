"""
Cog that impacts the core functionality of bot commands

Handles all guild-local command permissions
"""

# Import our requirements
from bot.cog_base import Base, commands
from bot.checks import is_admin, is_owner

# Custom command classes
from bot import command as NyaCommands

# Utility
from discord import Role as DiscordRole, utils as DiscordUtils


class setup(Base, name="Permissions"):
    def __init__(self):
        self.db = self.bot.database.collection("ServersJoined")

    def check_has_permission(self, ctx, of):
        # Find our guild in our database
        guild = self.db.find(guild_id=str(ctx.guild.id))

        # Check if mod_ or admin_ role IDs exist in guild store
        # Don't continue if they don't exist
        if f'{of}_role_ids' not in guild.getStore():
            return False

        # Loop over the role IDs in database, and if the author
        # has one of those roles, then return True
        for role_id in guild[f"{of}_role_ids"]:
            if DiscordUtils.get(ctx.author.roles, id=int(role_id)):
                return True

        return False

    def check_is_admin(self, ctx):
        return self.check_has_permission(ctx, "admin")

    def check_is_moderator(self, ctx):
        return self.check_has_permission(ctx, "mod")

    # Server permissions config
    # Only execute block below, if there's no sub-command
    @NyaCommands.group("config", invoke_without_command=True, protected=True)
    @is_admin()
    async def configure(self, ctx):
        await ctx.send_help(ctx.invoked_with)

    # Set moderator roles
    @NyaCommands.command("set_moderators")
    @is_admin()
    async def configure_set_moderator_roles(self, ctx, roles: commands.Greedy[DiscordRole]):
        # Find DB entry by ID, and update role IDs
        entry = self.db.find(guild_id=str(ctx.guild.id))
        entry["mod_role_ids"] = [str(role.id) for role in roles]
        entry.save()

        # Add reaction to message for success
        await ctx.message.add_reaction('👍')

    @NyaCommands.command("set_admins")
    @is_owner()
    async def configure_set_admin_roles(self, ctx, roles: commands.Greedy[DiscordRole]):
        # Find DB entry by ID, and update role IDs
        entry = self.db.find(guild_id=str(ctx.guild.id))
        entry["admin_role_ids"] = [str(role.id) for role in roles]
        entry.save()

        # Add reaction to message for success
        await ctx.message.add_reaction('👍')

    # Event to add new guilds to the database, or remove old ones
    @Base.listener()
    async def on_ready(self):
        # Get list of current guilds joined, and of current guilds in database
        guilds_joined = [guild.id for guild in self.bot.guilds]
        guilds_in_database = [int(guild["guild_id"]) for guild in self.db.entries]

        # Separate out the differences between the two lists
        differences = set(guilds_joined) ^ set(guilds_in_database)

        # Loop over all differences
        for guild_id in differences:
            # If guild isn't joined (meaning it's in the database only), remove from DB
            # If it is joined, and not in database, then just add it to DB
            if guild_id not in guilds_joined:
                self.db.find(guild_id=str(guild_id)).delete()
            else:
                self.db.enter(
                    dict(
                        guild_id=str(guild_id)
                    )
                )

    # Add a guild when we join it
    @Base.listener()
    async def on_guild_join(self, guild):
        self.db.enter(
            dict(
                guild_id=str(guild.id)
            )
        )

    # Remove a guild when we leave it (kicked, banned, left)
    @Base.listener()
    async def on_guild_remove(self, guild):
        self.db.find(guild_id=str(guild.id)).delete()

    # Command to enable commands that have been disabled
    @NyaCommands.command(protected=True)
    async def enable_command(self, ctx, *, command):
        # Find guild from database
        entry = self.db.find(guild_id=str(ctx.guild.id))

        # Only update if there are any disabled commands in the database store
        if "disabled_commands" in entry.getStore():
            # Remove command from the entry if it's inserted
            if command in entry["disabled_commands"]:
                entry["disabled_commands"].remove(command)

            entry.save()

        await ctx.message.add_reaction('👍')

    # Command to enable commands that have been disabled
    @NyaCommands.command(protected=True)
    async def disable_command(self, ctx, *, command):
        # Find guild from database
        entry = self.db.find(guild_id=str(ctx.guild.id))

        # Add disabled commands list into store
        if "disabled_commands" not in entry.getStore():
            entry["disabled_commands"] = []

        # Don't disable if command is protected
        bot_command: NyaCommands.NyaCommand = self.bot.get_command(command)
        if bot_command.protected:
            await ctx.send("You can't disable this command")
            return

        # Add command into disabled commands if it's not inserted
        if command not in entry["disabled_commands"]:
            entry["disabled_commands"].append(command)

        entry.save()
        await ctx.message.add_reaction('👍')
