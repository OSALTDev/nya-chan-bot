from discord.ext import commands
from discord.ext.commands import group
from cogs.base_cog import BaseCog


class Moderation(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)

    @group()
    async def mod(self, ctx):
        """Mod commands."""
        if ctx.invoked_subcommand is None:
            await ctx.author.send('Invalid mod command passed, {}'.format(ctx.author.mention))

    @mod.command(description='Promotes an user to be a Mod')
    @commands.has_any_role('Nixie', 'Supervisors')
    async def set(self, ctx, *username):
        """Promotes an user to be a Mod"""
        user_name = " ".join(username)
        converter = commands.converter.MemberConverter()
        user = await converter.convert(ctx, user_name)
        if user is None:
            await self.bot_reply(ctx, 'The user **{}** cannot be found, {}'.format(user_name, ctx.author.mention))
        mod_role = None
        moderator_role = None
        mod_trainee_role = None
        for role in ctx.guild.roles:
            if role.name == 'Mods':
                mod_role = role
            elif role.name == 'Mod Trainees':
                mod_trainee_role = role
            elif role.name == 'Moderators':
                moderator_role = role
        if mod_role is None:
            await self.bot_reply(ctx, 'The Mods role cannot be found, {}'.format(ctx.author.mention))
            return False
        if moderator_role is None:
            await self.bot_reply(ctx, 'The Moderators role cannot be found, {}'.format(ctx.author.mention))
            return False
        if mod_trainee_role is None:
            await self.bot_reply(ctx, 'The Mod Trainees role cannot be found, {}'.format(ctx.author.mention))
            return False
        has_mod_role = False
        has_trainee_role = False
        for user_role in user.roles:
            if user_role.name == 'Mods':
                has_mod_role = True
            elif user_role.name == 'Mod Trainees':
                has_trainee_role = True
        if has_mod_role is True:
            await self.bot_reply(ctx, '{} is a Mod already, {}'.format(user.name, ctx.author.mention))
            return False
        if has_trainee_role is True:
            await user.add_roles(mod_role, reason="Promoted to Mods")
            user.roles.append(mod_role)
            await user.remove_roles(mod_trainee_role, reason="Promoted to Mods")
        else:
            await user.add_roles(mod_role, moderator_role, reason="Promoted to Mods")
        await self.bot_reply(ctx, '{} is now a Mod, {}'.format(user.name, ctx.author.mention))

    @mod.command(description='Removes an user Mod status')
    @commands.has_any_role('Nixie', 'Supervisors')
    async def remove(self, ctx, *username):
        """Removes an user Mod status"""
        user_name = " ".join(username)
        converter = commands.converter.MemberConverter()
        user = await converter.convert(ctx, user_name)
        if user is None:
            await self.bot_reply(ctx, 'The user **{}** cannot be found, {}'.format(user_name, ctx.author.mention))
        mod_role = None
        moderator_role = None
        for role in ctx.guild.roles:
            if role.name == 'Mods':
                mod_role = role
            elif role.name == 'Moderators':
                moderator_role = role
        if mod_role is None:
            await self.bot_reply(ctx, 'The Mods role cannot be found, {}'.format(ctx.author.mention))
            return False
        if moderator_role is None:
            await self.bot_reply(ctx, 'The Moderators role cannot be found, {}'.format(ctx.author.mention))
            return False
        has_mod_role = False
        for user_role in user.roles:
            if user_role.name == 'Mods':
                has_mod_role = True
        if has_mod_role is not True:
            await self.bot_reply(ctx, '{} is a not a Mod, {}'.format(user.name, ctx.author.mention))
            return False
        await user.remove_roles(mod_role, moderator_role, reason="User demoted from Mods")
        await self.bot_reply(ctx, '{} is not a Mod anymore, {}'.format(user.name, ctx.author.mention))

    @mod.command(description='Promotes an user to be a Mod Trainee')
    @commands.has_any_role('Nixie', 'Supervisors')
    async def set_trainee(self, ctx, *username):
        """Promotes an user to be a Mod Trainee"""
        user_name = " ".join(username)
        converter = commands.converter.MemberConverter()
        user = await converter.convert(ctx, user_name)
        if user is None:
            await self.bot_reply(ctx, 'The user **{}** cannot be found, {}'.format(user_name, ctx.author.mention))
        mod_role = None
        moderator_role = None
        mod_trainee_role = None
        for role in ctx.guild.roles:
            if role.name == 'Mods':
                mod_role = role
            elif role.name == 'Mod Trainees':
                mod_trainee_role = role
            elif role.name == 'Moderators':
                moderator_role = role
        if mod_role is None:
            await self.bot_reply(ctx, 'The Mod role cannot be found, {}'.format(ctx.author.mention))
            return False
        if moderator_role is None:
            await self.bot_reply(ctx, 'The Moderators role cannot be found, {}'.format(ctx.author.mention))
            return False
        if mod_trainee_role is None:
            await self.bot_reply(ctx, 'The Mod Trainees role cannot be found, {}'.format(ctx.author.mention))
            return False
        has_mod_role = False
        has_trainee_role = False
        for user_role in user.roles:
            if user_role.name == 'Mods':
                has_mod_role = True
            elif user_role.name == 'Mod Trainees':
                has_trainee_role = True
        if has_trainee_role is True:
            await self.bot_reply(ctx, '{} is a Mod Trainee already, {}'.format(user.name, ctx.author.mention))
            return False
        if has_mod_role is True:
            await user.add_roles(mod_trainee_role, reason="Promoted to Mod Trainees")
            user.roles.append(mod_trainee_role)
            await user.remove_roles(mod_role, reason="Promoted to Mod Trainees")
        else:
            await user.add_roles(mod_trainee_role, moderator_role, reason="Promoted to Mod Trainees")
        await self.bot_reply(ctx, '{} is now a Mod Trainee, {}'.format(user.name, ctx.author.mention))

    @mod.command(description='Removes an user Mod Trainee status')
    @commands.has_any_role('Nixie', 'Supervisors')
    async def remove_trainee(self, ctx, *username):
        """Removes an user Mod Trainee status"""
        user_name = " ".join(username)
        converter = commands.converter.MemberConverter()
        user = await converter.convert(ctx, user_name)
        if user is None:
            await self.bot_reply(ctx, 'The user **{}** cannot be found, {}'.format(user_name, ctx.author.mention))
        mod_role = None
        moderator_role = None
        mod_trainee_role = None
        for role in ctx.guild.roles:
            if role.name == 'Mods':
                mod_role = role
            elif role.name == 'Mod Trainees':
                mod_trainee_role = role
            elif role.name == 'Moderators':
                moderator_role = role
        if mod_role is None:
            await self.bot_reply(ctx, 'The Mods role cannot be found, {}'.format(ctx.author.mention))
            return False
        if moderator_role is None:
            await self.bot_reply(ctx, 'The Moderators role cannot be found, {}'.format(ctx.author.mention))
            return False
        if mod_trainee_role is None:
            await self.bot_reply(ctx, 'The Mod Trainees role cannot be found, {}'.format(ctx.author.mention))
            return False
        has_trainee_role = False
        for user_role in user.roles:
            if user_role.name == 'Mod Trainees':
                has_trainee_role = True
        if has_trainee_role is not True:
            await self.bot_reply(ctx, '{} is a not a Mod Trainee, {}'.format(user.name, ctx.author.mention))
            return False
        await user.remove_roles(mod_trainee_role, moderator_role, reason="User demoted from Mod Trainees")
        await self.bot_reply(ctx, '{} is not a Mod Trainee anymore, {}'.format(user.name, ctx.author.mention))


def setup(bot):
    cog = Moderation(bot)
    bot.add_cog(cog)
