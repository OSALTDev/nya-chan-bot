import discord
from discord.ext import commands
from cogs.base_cog import BaseCog
import datetime
import pytz
from database import Methods as db_util


class Cog(BaseCog, name="Profiles"):
    """Let users have a more detailed profile. (including timezone !)"""
    @commands.group(invoke_without_command=True)
    async def p(self, ctx):
        """Profile commands."""
        # Couldnt this just be removed ?
        await self.no_invoke_help(ctx)

    @commands.group(invoke_without_command=True)
    async def tz(self, ctx):
        """Timezone commands."""
        await self.no_invoke_help(ctx)

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
            cursor.execute(*db_util.select("profiles").items("id").limit(1).where(id_user=ctx.author.id).build)
            row = cursor.fetchone()

        with self.cursor_context(commit=True) as cursor:
            if not row:
                cursor.execute(*db_util.insert("profiles").items(id_user=ctx.author.id, timezone=tz_name).build)
            else:
                cursor.execute(*db_util.update("profiles").items(timezone=tz_name).where(id=row[0]).build)

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
            cursor.execute(*db_util.select("profiles").items("timezone").where(id_user=user.id).build)
            row = cursor.fetchone()

        if not row:
            await ctx.reply(f'The user **{user.name}** has not set his timezone')
            return
        tz_name = row[0]

        local_tz = pytz.timezone(tz_name)
        time_now_localized = time_now_utc.astimezone(local_tz)
        time_now_formatted = time_now_localized.strftime('%Y-%m-%d %H:%M:%S')
        await ctx.reply(f'**{user.name}**\'s local time is **{time_now_formatted}**')

