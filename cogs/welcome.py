from bot.cog_base import Base, commands
import discord


class setup(Base, name="Welcome"):
    def __init__(self):
        self.db = self.bot.database.collection("WelcomeMessages")

    @Base.listener()
    async def on_member_join(self, member):
        entry = self.db.entry(str(member.guild.id))
        if entry:
            try:
                await member.send(entry["welcome_message"])
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
