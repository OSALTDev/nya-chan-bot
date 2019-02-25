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
            await ctx.reply(f'The timezone "**{tz_name}**" does not exist')
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
        time_now_formatted = time_now_localized.strftime('%Y-%m-%d %H:%M:%S')
        await ctx.reply(f'Your timezone has been set to "**{tz_name}**", your local time is **{time_now_formatted}**')

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
                'List of available timezone areas : `{}`'.format(', '.join(tz_areas)))
        else:
            if area in tz_dict:
                await ctx.reply(
                    'List of available timezones for area **{}** : `{}`'
                    .format(area, ', '.join(sorted(tz_dict[area]))))
            else:
                await ctx.reply(f'The area **{area}** has not been found')

    @commands.command(description='Displays a user local time')
    @commands.guild_only()
    async def time(self, ctx, user: discord.Member):
        """Displays a user local time"""
        utc = pytz.utc
        time_now = datetime.datetime.utcnow()
        time_now_utc = utc.localize(time_now)

        with self.cursor_context() as cursor:
            cursor.execute("""SELECT `timezone` FROM `profiles` WHERE `id_user` = %s""", user.id)
            row = cursor.fetchone()

        if not row:
            await ctx.reply(f'The user **{user.name}** has not set his timezone')
            return
        tz_name = row[0]

        local_tz = pytz.timezone(tz_name)
        time_now_localized = time_now_utc.astimezone(local_tz)
        time_now_formatted = time_now_localized.strftime('%Y-%m-%d %H:%M:%S')
        await ctx.reply(f'**{user.name}**\'s local time is **{time_now_formatted}**')


def setup(bot):
    cog = Profiles(bot)
    bot.add_cog(cog)
