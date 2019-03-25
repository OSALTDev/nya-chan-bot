import discord
from discord.ext import commands
from cogs.base_cog import BaseCog
from nyalib.NyaBot import ThrowawayException
from types import SimpleNamespace
import functools


class Cog(BaseCog, name="Moderation"):
    def __init__(self, bot):
        super().__init__(bot)
        self._set_mod = SetMod("Mod", "mod", "trainee")
        self._set_trainee = SetMod("Mod Trainee", "trainee", "mod")
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
        if not ctx.subcommand_passed:
            return

        if ctx.command.callback.__name__ in self.roles:
            # If a set or remove command
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
        await ctx.send_help("mod")

    @mod.group(invoke_without_command=True, description='Promotes an user to be a Mod')
    async def set(self, ctx, user: discord.Member):
        """Promotes an user to be a Mod"""
        await self._set_mod(ctx, user, True)

    @mod.group(invoke_without_command=True, description='Removes an user Mod status')
    async def remove(self, ctx, user: discord.Member):
        """Removes an user Mod status"""
        await self._set_mod(ctx, user, False)

    @set.command(name="trainee", description='Promotes an user to be a Mod Trainee')
    async def set_trainee(self, ctx, user: discord.Member):
        """Promotes an user to be a Mod Trainee"""
        await self._set_trainee(ctx, user, True)

    @remove.command(name="trainee", description='Removes an user Mod Trainee status')
    async def remove_trainee(self, ctx, user: discord.Member):
        """Removes an user Mod Trainee status"""
        await self._set_trainee(ctx, user, False)

    @mod.group(invoke_without_command=True, description="Setup mod roles")
    async def roles(self, ctx):
        pass

    @roles.command(name="mod", description="Set the roles for core Mod role")
    async def mod_role(self, ctx, primary_role: discord.Role,
                       secondary_roles: commands.Greedy[discord.Role] = None):
        pass

    @roles.command(name="trainee", description="Set the roles for trainee moderator (displayed separately)")
    async def trainee_role(self, ctx, primary_role: discord.Role,
                           secondary_roles: commands.Greedy[discord.Role] = None):
        pass

    @roles.command(name="moderator", description="Set the roles for macho moderator (displayed separately)")
    async def moderator_role(self, ctx, primary_role: discord.Role,
                             secondary_roles: commands.Greedy[discord.Role] = None):
        pass


class SetMod:
    __slots__ = ('_name', '_add', '_rem')

    def __init__(self, role_name, role_to_add, role_to_remove):
        self._name = role_name
        self._add = role_to_add
        self._rem = role_to_remove

    async def __call__(self, ctx, user, action):
        if action is True:
            if getattr(ctx.custom.has_role, self._add) is True:
                await ctx.reply(f'{user.name} is a {self._name} already')
                return

            if getattr(ctx.custom.has_role, self._rem) is True:
                await user.add_roles(getattr(ctx.custom.roles, self._add), reason="Promoted to Mods")
                await user.remove_roles(getattr(ctx.custom.roles, self._rem), reason="Promoted to Mods")
            else:
                await user.add_roles(getattr(ctx.custom.roles, self._add), ctx.custom.roles.moderator,
                                     reason=f"Promoted to {self._name}s")
            await ctx.reply(f'{user.name} is now a {self._name}')
        else:
            if getattr(ctx.custom.has_role, self._add) is False:
                await ctx.reply(f'{user.name} is a not a {self._name}')
                return

            await user.remove_roles(getattr(ctx.custom.roles, self._add), ctx.custom.roles.moderator,
                                    reason=f"User demoted from {self._name}")
            await ctx.reply(f'{user.name} is not a {self._name} anymore')
