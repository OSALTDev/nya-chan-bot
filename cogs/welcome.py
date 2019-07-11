from bot.cog_base import Base, commands
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

    @commands.group(invoke_without_command=True)
    async def welcome(self, ctx: commands.Context):
        await ctx.send_help(ctx.invoked_with)

    @welcome.command(name="toggle")
    async def welcome_toggle(self, ctx):
        entry = self.db.entry(str(ctx.guild.id))
        enabled = True
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

        actioned = "enabled" if enabled else "disabled"
        await ctx.send(f"The welcome message for this guild is now {actioned}")

    @welcome.command(name="roles")
    async def welcome_roles(self, ctx, roles: commands.Greedy[discord.Role]):
        entry = self.db.entry(str(ctx.guild.id))
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

        embed = discord.Embed(
            title="New auto-roles",
            description=", ".join(role.name for role in roles)
        )
        await ctx.send("You have updated your automatic role setting", embed=embed)

    @welcome.command(name="message")
    async def welcome_message(self, ctx, *, message: str = None):
        entry = self.db.entry(str(ctx.guild.id))

        if message:
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

            embed = discord.Embed(
                title="New Welcome Message",
                description=message
            )
            await ctx.send("Your welcome message has been set", embed=embed)
            return

        if not entry:
            await ctx.send("No welcome message is set")
            return

        embed = discord.Embed(
            title="Welcome Message",
            description=entry["welcome_message"]
        )
        await ctx.send(embed=embed)
