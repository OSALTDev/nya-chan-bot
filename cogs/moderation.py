import discord
from discord.ext import commands
from cogs.base_cog import BaseCog
from nyalib.NyaBot import ThrowawayException
from types import SimpleNamespace
import functools


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

    async def cog_check(self, ctx):
        if ctx.guild is None:
            raise commands.NoPrivateMessage('This command cannot be used in private messages.')
        getter = functools.partial(discord.utils.get, ctx.author.roles)
        return any(getter(name=item) is not None for item in ('Nixie', 'Supervisors'))

    async def cog_before_invoke(self, ctx):
        if ctx.subcommand_passed:
            user = ctx.args[2]
            command_name = ctx.command.callback.__name__

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

    @mod.group(invoke_without_command=True, description='Promotes an user to be a Mod')
    async def set(self, ctx, user: discord.Member):
        """Promotes an user to be a Mod"""
        if ctx.custom.has_role.mod is True:
            await ctx.reply(f'{user.name} is a Mod already')
            return

        if ctx.custom.has_role.trainee is True:
            await user.add_roles(ctx.custom.roles.mod, reason="Promoted to Mods")
            await user.remove_roles(ctx.custom.roles.trainee, reason="Promoted to Mods")
        else:
            await user.add_roles(ctx.custom.roles.mod, ctx.custom.roles.moderator, reason="Promoted to Mods")
        await ctx.reply(f'{user.name} is now a Mod')

    @mod.group(invoke_without_command=True, description='Removes an user Mod status')
    async def remove(self, ctx, user: discord.Member):
        """Removes an user Mod status"""
        if ctx.custom.has_role.mod is False:
            await ctx.reply(f'{user.name} is a not a Mod')
            return

        await user.remove_roles(ctx.custom.roles.mod, ctx.custom.roles.moderator, reason="User demoted from Mods")
        await ctx.reply(f'{user.name} is not a Mod anymore')

    @set.command(name="trainee", description='Promotes an user to be a Mod Trainee')
    async def set_trainee(self, ctx, user: discord.Member):
        """Promotes an user to be a Mod Trainee"""
        if ctx.custom.has_role.trainee is True:
            await ctx.reply(f'{user.name} is a Mod Trainee already')
            return

        if ctx.custom.has_role.mod is True:
            await user.add_roles(ctx.custom.roles.trainee, reason="Promoted to Mod Trainees")
            await user.remove_roles(ctx.custom.roles.mod, reason="Promoted to Mod Trainees")
        else:
            await user.add_roles(ctx.custom.roles.trainee, ctx.custom.roles.moderator, reason="Promoted to Mod Trainees")
        await ctx.reply(f'{user.name} is now a Mod Trainee')

    @remove.command(name="trainee", description='Removes an user Mod Trainee status')
    async def remove_trainee(self, ctx, user: discord.Member):
        """Removes an user Mod Trainee status"""
        if ctx.custom.has_role.trainee is False:
            await ctx.reply(f'{user.name} is a not a Mod Trainee')
            return

        await user.remove_roles(ctx.custom.roles.trainee, ctx.custom.roles.moderator, reason="User demoted from Mod Trainees")
        await ctx.reply(f'{user.name} is not a Mod Trainee anymore')


def setup(bot):
    cog = Moderation(bot)
    bot.add_cog(cog)
