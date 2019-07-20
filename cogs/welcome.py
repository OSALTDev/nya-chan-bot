"""
Cog that handles messaging and setting roles on new members

Allows guild admins to disable messaging/autorole and setup custom messages and roles for new users
"""

# Import requirements
from bot.cog_base import Base, commands
from bot.checks import is_admin

# Custom commands
from bot import command as NyaCommand

# Discord.py library
import discord


class setup(Base, name="Welcome"):
    def __init__(self):
        self.db = self.bot.database.collection("WelcomeMessages")

    @Base.listener()
    async def on_member_join(self, member: discord.Member):
        entry = self.db.entry(str(member.guild.id))
        if entry:
            try:
                if "welcome_message" in entry.getStore():
                    await member.send(entry["welcome_message"])

                if "roles" in entry.getStore():
                    roles = [discord.utils.get(member.guild.roles, id=int(role_id)) for role_id in entry["roles"]]
                    await member.add_roles(*roles, reason="Automatic role assignment")
            except discord.Forbidden:
                pass

    # Guild welcome config
    # Only execute block below, if there's no sub-command
    @NyaCommand.group(invoke_without_command=True)
    @is_admin()
    async def welcome(self, ctx: commands.Context):
        await ctx.send_help(ctx.invoked_with)

    # Command to enable or disable welcome messaging
    @welcome.command(name="toggle")
    @is_admin()
    async def welcome_toggle(self, ctx):
        # Get guild entry from database
        entry = self.db.entry(str(ctx.guild.id))

        # Enabled by default
        enabled = True

        # If entry doesn't exist, just enable welcoming
        # If not, toggle between enabled and disabled
        if not entry:
            self.db.enter(
                {"welcome_enable": True},
                str(ctx.guild.id)
            )
        else:
            enabled = not entry["welcome_enabled"]
            self.db.update(
                str(ctx.guild.id),
                {"welcome_enable": enabled}
            )

        # Send message based on if enabled or not
        actioned = "enabled" if enabled else "disabled"
        await ctx.send(f"The welcome message for this guild is now {actioned}")

    # Set welcome auto-roles
    @welcome.command(name="roles")
    @is_admin()
    async def welcome_roles(self, ctx, roles: commands.Greedy[discord.Role]):
        # Get guild entry
        entry = self.db.entry(str(ctx.guild.id))

        # If the entry exists, update it
        # If it doesn't, insert it
        if entry:
            self.db.update(
                str(ctx.guild.id),
                {"roles": [str(role.id) for role in roles]}
            )
        else:
            self.db.enter(
                {"roles": [str(role.id) for role in roles]},
                str(ctx.guild.id)
            )

        # Construct embed to list roles added
        embed = discord.Embed(
            title="New auto-roles",
            description=", ".join(role.name for role in roles)
        )
        await ctx.send("You have updated your automatic role setting", embed=embed)

    # Set welcome message
    @welcome.command(name="message")
    @is_admin()
    async def welcome_message(self, ctx, *, message: str = None):
        # Get guild entry
        entry = self.db.entry(str(ctx.guild.id))

        # If there's a message argument, insert or add entry into database
        if message:
            # If entry doesn't exist, insert entry
            # If it does, then update
            if not entry:
                self.db.enter(
                    {"welcome_message": message},
                    str(ctx.guild.id)
                )
            else:
                self.db.update(
                    str(ctx.guild.id),
                    {"welcome_message": message}
                )

            # Construct embed to display welcome message
            embed = discord.Embed(
                title="New Welcome Message",
                description=message
            )
            await ctx.send("Your welcome message has been set", embed=embed)
            return

        # If entry isn't set, display that entry doesn't exist
        if not entry:
            await ctx.send("No welcome message is set")
            return

        # Construct embed to display welcome message
        embed = discord.Embed(
            title="Welcome Message",
            description=entry["welcome_message"]
        )
        await ctx.send(embed=embed)
