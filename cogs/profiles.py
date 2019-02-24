import discord
from discord.ext import commands
from cogs.base_cog import BaseCog
import datetime
import pytz


class Profiles(BaseCog):
    """Let users have a more detailed profile. (including timezone !)"""
    @commands.group(invoke_without_command=True)
    async def p(self, ctx):
        """Profile commands."""
        # Couldnt this just be removed ?
        await ctx.invoke(self.bot.get_command("help"), ctx.invoked_with)

    @commands.group(invoke_without_command=True)
    async def tz(self, ctx):
        """Timezone commands."""
        await ctx.invoke(self.bot.get_command("help"), ctx.invoked_with)

    @tz.command(description='Set timezone.')
    @commands.guild_only()
    async def set(self, ctx, tz_name: str):
        """Set your current timezone"""
        try:
            local_tz = pytz.timezone(tz_name)
        except pytz.exceptions.UnknownTimeZoneError:
            await ctx.reply('The timezone "**{}**" does not exist, {}'.format(tz_name, ctx.author.mention))
            return

        with self.cursor_context(commit=True) as cursor:
            cursor.execute("""SELECT `id` FROM `profiles` WHERE `id_user` = %s""", ctx.author.id)
            row = cursor.fetchone()
            if not row:
                cursor.execute(
                    "INSERT INTO profiles (id, id_user, timezone) VALUES (null, %s, %s)",
                    (ctx.author.id, tz_name))
            else:
                cursor.execute(
                    "UPDATE profiles SET timezone = %s WHERE id = %s",
                    (tz_name, row[0]))

        utc = pytz.utc
        time_now = datetime.datetime.utcnow()
        time_now_utc = utc.localize(time_now)
        time_now_localized = time_now_utc.astimezone(local_tz)
        await ctx.reply(
            'Your timezone has been set to "**{}**", '
            'your local time is **{}**, {}'.format(
                tz_name, time_now_localized.strftime('%Y-%m-%d %H:%M:%S'), ctx.author.mention
            ))

    @tz.command(description='List timezones.')
    @commands.guild_only()
    async def list(self, ctx, area: str = None):
        """List your current timezone"""
        tz_dict = {}
        for tz in pytz.common_timezones:
            try:
                tz_left, tz_right = map(str, tz.split('/'))
            except Exception:
                continue
            else:
                if tz_left not in tz_dict:
                    tz_dict[tz_left] = set()
                tz_dict[tz_left].add(tz_right)

        tz_areas = list(tz_dict.keys())
        tz_areas.sort()
        if area is None:
            await ctx.reply(
                'List of available timezone areas : `{}`, {}'.format(', '.join(tz_areas), ctx.author.mention))
        else:
            if area in tz_dict:
                await ctx.reply(
                    'List of available timezones for area **{}** : `{}`, {}'
                    .format(area, ', '.join(sorted(tz_dict[area])), ctx.author.mention))
            else:
                await ctx.reply('The area **{}** has not been found, {}'.format(area, ctx.author.mention))

    @commands.command(description='Displays a user local time')
    @commands.guild_only()
    async def time(self, ctx, user: discord.Member = None):
        """Displays a user local time"""
        if user is None:
            await ctx.reply('The user **{}** cannot be found, {}'.format(user, ctx.author.mention))
            return

        utc = pytz.utc
        time_now = datetime.datetime.utcnow()
        time_now_utc = utc.localize(time_now)

        with self.cursor_context() as cursor:
            cursor.execute("""SELECT `timezone` FROM `profiles` WHERE `id_user` = %s""", user.id)
            row = cursor.fetchone()

        if not row:
            await ctx.reply('The user **{}** has not set his timezone, {}'.format(user.name, ctx.author.mention))
            return
        tz_name = row[0]

        local_tz = pytz.timezone(tz_name)
        time_now_localized = time_now_utc.astimezone(local_tz)
        await ctx.reply(
            '**{}**\'s local time is **{}**, {}'.format(user.name, time_now_localized.strftime('%Y-%m-%d %H:%M:%S'),
                                                        ctx.author.mention))


def setup(bot):
    cog = Profiles(bot)
    bot.add_cog(cog)
