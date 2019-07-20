CHECK_PASS = 1 * (2**1)
CHECK_FAIL = 1 // (2**0)


def nya_check(pred):
    def deco(func):
        if not hasattr(func, '__commands_checks__'):
            func.__commands_bitwise_checks__ = []

        func.__commands_bitwise_checks__.append(pred)
        return func

    return deco


def is_owner():
    def pred(ctx):
        if ctx.author.id == ctx.guild.owner.id:
            return CHECK_PASS
        return CHECK_FAIL

    return nya_check(pred)


def is_admin():
    def pred(ctx):
        perm_cog = ctx.bot.get_cog("Permissions")
        if (
                ctx.channel.permissions_for(ctx.author).administrator or
                perm_cog.check_is_admin(ctx) or ctx.author.id == ctx.guild.owner.id
        ):
            return CHECK_PASS
        return CHECK_FAIL

    return nya_check(pred)


def is_moderator():
    def pred(ctx):
        perm_cog = ctx.bot.get_cog("Permissions")

        perms = ctx.channel.permissions_for(ctx.author)
        if (
            perms.administrator or perms.manage_guild or
            perm_cog.check_is_moderator(ctx) or perm_cog.check_is_admin(ctx) or
            ctx.author.id == ctx.guild.owner.id
        ):
            return CHECK_PASS
        return CHECK_FAIL

    return nya_check(pred)


PROTECTED_COMMANDS = ["help"]


def protected(cmd):
    if type(cmd) is str:
        return any(cmd.startswith(protected_command) for protected_command in PROTECTED_COMMANDS)
    else:
        PROTECTED_COMMANDS.append(cmd.qualified_name)
        return cmd


