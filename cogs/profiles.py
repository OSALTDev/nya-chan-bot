from discord.ext import commands
from discord.ext.commands import group
from cogs.base_cog import BaseCog
import datetime
import math
import pytz


class Profiles(BaseCog):
    """Let users have a more detailed profile. (including timezone !)"""

    def __init__(self, bot):
        super().__init__(bot)

    @group()
    async def p(self, ctx):
        """Profile commands."""
        bot_channel = self.bot.get_channel(332644650462478336)
        if bot_channel is None:
            await ctx.channel.send('The dedicated bot commands channel cannot be found')
            return False
        if ctx.invoked_subcommand is None:
            await bot_channel.send('Invalid profile command passed, {}'.format(ctx.author.mention))

    @group()
    async def tz(self, ctx):
        """Timezone commands."""
        bot_channel = self.bot.get_channel(332644650462478336)
        if bot_channel is None:
            await ctx.channel.send('The dedicated bot commands channel cannot be found')
            return False
        if ctx.invoked_subcommand is None:
            await bot_channel.send('Invalid timezone command passed, {}'.format(ctx.author.mention))

    @tz.command(description='Set timezone.')
    @commands.guild_only()
    async def set(self, ctx, tz_name: str):
        """Set your current timezone"""
        bot_channel = self.bot.get_channel(332644650462478336)
        if bot_channel is None:
            await ctx.channel.send('The dedicated bot commands channel cannot be found')
            return False
        try:
            local_tz = pytz.timezone(tz_name)
        except pytz.exceptions.UnknownTimeZoneError:
            await bot_channel.send('The timezone "**{}**" does not exist, {}'.format(tz_name, ctx.author.mention))
            return False
        connection = self.config.db_connection()
        cursor = connection.cursor()
        cursor.execute("""SELECT `id` FROM `profiles` WHERE `id_user` = %s""", ctx.author.id)
        rows = cursor.fetchall()
        if len(rows) == 0:
            cursor.execute(
                """INSERT INTO profiles (id, id_user, timezone) VALUES (null, %s, %s)""",
                (ctx.author.id, tz_name))
        else:
            cursor.execute(
                """UPDATE profiles SET timezone = %s WHERE id = %s""",
                (tz_name, rows[0][0]))
        connection.commit()
        utc = pytz.utc
        time_now = datetime.datetime.utcnow()
        time_now_utc = utc.localize(time_now)
        time_now_localized = time_now_utc.astimezone(local_tz)
        await bot_channel.send(
            'Your timezone has been set to "**{}**", your local time is **{}**, {}'.format(tz_name,
                                                                                           time_now_localized.strftime(
                                                                                               '%Y-%m-%d %H:%M:%S'),
                                                                                           ctx.author.mention))

    @tz.command(description='List timezones.')
    @commands.guild_only()
    async def list(self, ctx, area: str = None):
        """List your current timezone"""
        bot_channel = self.bot.get_channel(332644650462478336)
        if bot_channel is None:
            await ctx.channel.send('The dedicated bot commands channel cannot be found')
            return False
        tz_dict = {}
        for tz in pytz.common_timezones:
            try:
                tz_left, tz_right = map(str, tz.split('/'))
            except Exception:
                continue
            if tz_left not in tz_dict:
                tz_dict[tz_left] = set()
            tz_dict[tz_left].add(tz_right)
        tz_areas = list(tz_dict.keys())
        tz_areas.sort()
        if area is None:
            await bot_channel.send(
                'List of available timezone areas : `{}`, {}'.format(', '.join(tz_areas), ctx.author.mention))
        else:
            if area in tz_dict:
                await bot_channel.send(
                    'List of available timezones for area **{}** : `{}`, {}'.format(area,
                                                                                    ', '.join(sorted(tz_dict[area])),
                                                                                    ctx.author.mention))
            else:
                await bot_channel.send('The area **{}** has not been found, {}'.format(area, ctx.author.mention))

    @commands.command(description='Displays a user local time')
    @commands.guild_only()
    async def time(self, ctx, username: str):
        """Displays a user local time"""
        bot_channel = self.bot.get_channel(332644650462478336)
        if bot_channel is None:
            await ctx.channel.send('The dedicated bot commands channel cannot be found')
            return False
        converter = commands.converter.MemberConverter()
        user = await converter.convert(ctx, username)
        if user is None:
            await bot_channel.send('The user **{}** cannot be found, {}'.format(username, ctx.author.mention))
            return False
        utc = pytz.utc
        time_now = datetime.datetime.utcnow()
        time_now_utc = utc.localize(time_now)
        connection = self.config.db_connection()
        cursor = connection.cursor()
        cursor.execute("""SELECT `timezone` FROM `profiles` WHERE `id_user` = %s""", user.id)
        rows = cursor.fetchall()
        if len(rows) == 0:
            await bot_channel.send('The user **{}** has not set his timezone, {}'.format(user.name, ctx.author.mention))
            return False
        tz_name = rows[0][0]
        local_tz = pytz.timezone(tz_name)
        time_now_localized = time_now_utc.astimezone(local_tz)
        await bot_channel.send(
            '**{}**\'s local time is **{}**, {}'.format(user.name, time_now_localized.strftime('%Y-%m-%d %H:%M:%S'),
                                                        ctx.author.mention))


def setup(bot):
    cog = Profiles(bot)
    bot.add_cog(cog)
