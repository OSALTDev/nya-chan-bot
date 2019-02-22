import discord
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
    async def set(self, ctx, *, username: str):
        """Promotes an user to be a Mod"""
        converter = commands.converter.MemberConverter()
        user = await converter.convert(ctx, username)
        if user is None:
            await self.bot_reply(ctx, 'The user **{}** cannot be found, {}'.format(username, ctx.author.mention))
            return

        mod_role = discord.utils.get(ctx.guild.roles, name="Mods")
        moderator_role = discord.utils.get(ctx.guild.roles, name="Moderators")
        mod_trainee_role = discord.utils.get(ctx.guild.roles, name="Mod Trainees")

        unfound = []
        if mod_role is None:
            unfound.append("Mods")
        if moderator_role is None:
            unfound.append("Moderators")
        if mod_trainee_role is None:
            unfound.append("Mod Trainees")

        if unfound:
            await self.bot_reply(ctx, 'These roles cannot be found, {}: '.format(ctx.author.mention))
            return False

        has_mod_role = discord.utils.get(user.roles, name="Mods") is not None
        has_trainee_role = discord.utils.get(user.roles, name="Mod Trainees") is not None
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
    async def remove(self, ctx, *, username):
        """Removes an user Mod status"""
        converter = commands.converter.MemberConverter()
        user = await converter.convert(ctx, username)
        if user is None:
            await self.bot_reply(ctx, 'The user **{}** cannot be found, {}'.format(username, ctx.author.mention))
            return

        mod_role = discord.utils.get(ctx.guild.roles, name="Mods")
        moderator_role = discord.utils.get(ctx.guild.roles, name="Moderators")

        unfound = []
        if mod_role is None:
            unfound.append("Mods")
        if moderator_role is None:
            unfound.append("Moderators")

        if unfound:
            await self.bot_reply(ctx, 'These roles cannot be found, {}: {}'.format(ctx.author.mention, ", ".join(unfound)))
            return

        has_mod_role = discord.utils.get(user.roles, name="Mods") is not None
        if has_mod_role is False:
            await self.bot_reply(ctx, '{} is a not a Mod, {}'.format(user.name, ctx.author.mention))
            return

        await user.remove_roles(mod_role, moderator_role, reason="User demoted from Mods")
        await self.bot_reply(ctx, '{} is not a Mod anymore, {}'.format(user.name, ctx.author.mention))

    @mod.command(description='Promotes an user to be a Mod Trainee')
    @commands.has_any_role('Nixie', 'Supervisors')
    async def set_trainee(self, ctx, *, username):
        """Promotes an user to be a Mod Trainee"""
        converter = commands.converter.MemberConverter()
        user = await converter.convert(ctx, username)
        if user is None:
            await self.bot_reply(ctx, 'The user **{}** cannot be found, {}'.format(username, ctx.author.mention))
            return

        mod_role = discord.utils.get(ctx.guild.roles, name="Mods")
        moderator_role = discord.utils.get(ctx.guild.roles, name="Moderators")
        mod_trainee_role = discord.utils.get(ctx.guild.roles, name="Mod Trainees")

        unfound = []
        if mod_role is None:
            unfound.append("Mods")
        if moderator_role is None:
            unfound.append("Moderators")
        if mod_trainee_role is None:
            unfound.append("Mod Trainees")

        if unfound:
            await self.bot_reply(ctx, 'These roles cannot be found, {}: '.format(ctx.author.mention))
            return

        has_trainee_role = discord.utils.get(user.roles, name="Mod Trainees") is not None
        if has_trainee_role is True:
            await self.bot_reply(ctx, '{} is a Mod Trainee already, {}'.format(user.name, ctx.author.mention))
            return

        has_mod_role = discord.utils.get(user.roles, name="Mods") is not None
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

        mod_role = discord.utils.get(ctx.guild.roles, name="Mods")
        moderator_role = discord.utils.get(ctx.guild.roles, name="Moderators")
        mod_trainee_role = discord.utils.get(ctx.guild.roles, name="Mod Trainees")

        unfound = []
        if mod_role is None:
            unfound.append("Mods")
        if moderator_role is None:
            unfound.append("Moderators")
        if mod_trainee_role is None:
            unfound.append("Mod Trainees")

        if unfound:
            await self.bot_reply(ctx, 'These roles cannot be found, {}: '.format(ctx.author.mention))
            return

        has_trainee_role = discord.utils.get(user.roles, name="Mod Trainees") is not None
        if has_trainee_role is False:
            await self.bot_reply(ctx, '{} is a not a Mod Trainee, {}'.format(user.name, ctx.author.mention))
            return

        await user.remove_roles(mod_trainee_role, moderator_role, reason="User demoted from Mod Trainees")
        await self.bot_reply(ctx, '{} is not a Mod Trainee anymore, {}'.format(user.name, ctx.author.mention))


def setup(bot):
    cog = Moderation(bot)
    bot.add_cog(cog)
