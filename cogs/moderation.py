import discord
from discord.ext import commands
from cogs.base_cog import BaseCog
from nyalib.NyaBot import ThrowawayException
from types import SimpleNamespace


class Moderation(BaseCog, name="Moderation"):
    def __init__(self, bot):
        super().__init__(bot)
        self.roles = {
            "set": {
                "Mods": SimpleNamespace(name="mod", checked=True),
                "Moderators": SimpleNamespace(name="moderator", checked=False),
                "Mod Trainees": SimpleNamespace(name="trainee", checked=True)
            },
            "remove": {
                "Mods": SimpleNamespace(name="mod", checked=True),
                "Moderators": SimpleNamespace(name="moderator", checked=True)
            },
            "set_trainee": {
                "Mods": SimpleNamespace(name="mod", checked=True),
                "Moderators": SimpleNamespace(name="moderator", checked=False),
                "Mod Trainees": SimpleNamespace(name="trainee", checked=True)
            },
            "remove_trainee": {
                "Mods": SimpleNamespace(name="mod", checked=False),
                "Moderators": SimpleNamespace(name="moderator", checked=False),
                "Mod Trainees": SimpleNamespace(name="trainee", checked=True)
            }
        }

    async def cog_before_invoke(self, ctx):
        if ctx.invoked_subcommand is not None:
            user = ctx.kwargs.get("user")
            command_name = ctx.invoked_subcommand.name

            missing = []
            roles = SimpleNamespace()
            has_roles = SimpleNamespace()
            for role_name, attribute in self.roles[command_name].items():
                role = discord.utils.get(ctx.guild.roles, name=role_name)
                if not role:
                    missing.append(role_name)
                    continue

                if attribute.checked:
                    setattr(has_roles, attribute.name, discord.utils.get(user.roles, name=role_name) is not None)
                setattr(roles, attribute.name, role)

            if missing:
                await ctx.reply('These roles cannot be found: {}'.format(", ".join(missing)))
                raise ThrowawayException

            ctx.custom["roles"] = roles
            ctx.custom["has_role"] = has_roles

    @commands.group(invoke_without_command=True)
    async def mod(self, ctx):
        """Mod commands."""
        await ctx.invoke(self.bot.get_command("help"), ctx.invoked_with)

    @mod.command(description='Promotes an user to be a Mod')
    @commands.has_any_role('Nixie', 'Supervisors')
    async def set(self, ctx, *, user: discord.Member = None):
        """Promotes an user to be a Mod"""
        if ctx.custom.has_role.mod is True:
            await ctx.reply('{} is a Mod already'.format(user))
            return

        if ctx.custom.has_role.trainee is True:
            await user.add_roles(ctx.custom.roles.mod, reason="Promoted to Mods")
            await user.remove_roles(ctx.custom.roles.trainee, reason="Promoted to Mods")
        else:
            await user.add_roles(ctx.custom.roles.mod, ctx.custom.roles.moderator, reason="Promoted to Mods")
        await ctx.reply('{} is now a Mod'.format(user.name))

    @mod.command(description='Removes an user Mod status')
    @commands.has_any_role('Nixie', 'Supervisors')
    async def remove(self, ctx, *, user: discord.Member):
        """Removes an user Mod status"""
        if ctx.custom.has_role.mod is False:
            await ctx.reply('{} is a not a Mod'.format(user.name))
            return

        await user.remove_roles(ctx.custom.roles.mod, ctx.custom.roles.moderator, reason="User demoted from Mods")
        await ctx.reply('{} is not a Mod anymore'.format(user.name))

    @mod.command(description='Promotes an user to be a Mod Trainee')
    @commands.has_any_role('Nixie', 'Supervisors')
    async def set_trainee(self, ctx, *, user: discord.Member):
        """Promotes an user to be a Mod Trainee"""
        if ctx.custom.has_role.trainee is True:
            await ctx.reply('{} is a Mod Trainee already'.format(user))
            return

        if ctx.custom.has_role.mod is True:
            await user.add_roles(ctx.custom.roles.trainee, reason="Promoted to Mod Trainees")
            await user.remove_roles(ctx.custom.roles.mod, reason="Promoted to Mod Trainees")
        else:
            await user.add_roles(ctx.custom.roles.trainee, ctx.custom.roles.moderator, reason="Promoted to Mod Trainees")
        await ctx.reply('{} is now a Mod Trainee'.format(user.name))

    @mod.command(description='Removes an user Mod Trainee status')
    @commands.has_any_role('Nixie', 'Supervisors')
    async def remove_trainee(self, ctx, *, user: discord.Member = None):
        """Removes an user Mod Trainee status"""
        if ctx.custom.has_role.trainee is False:
            await ctx.reply('{} is a not a Mod Trainee'.format(user.name))
            return

        await user.remove_roles(ctx.custom.roles.trainee, ctx.custom.roles.moderator, reason="User demoted from Mod Trainees")
        await ctx.reply('{} is not a Mod Trainee anymore'.format(user.name))


def setup(bot):
    cog = Moderation(bot)
    bot.add_cog(cog)
