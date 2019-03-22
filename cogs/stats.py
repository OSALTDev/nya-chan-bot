from cogs.base_cog import BaseCog
from discord.ext import commands
from database import Methods as db_util
from database import DBFunction


class Stats(BaseCog):
    """Keep track of the amount of messages everyone send"""
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.content.startswith(self.bot.command_prefix) and not message.author.bot:
            guild = message.guild
            author = message.author
            channel = message.channel
            if guild is not None:
                with self.cursor_context() as cursor:
                    cursor.execute(*db_util.select("statistics_global").items("id", "msg_count")
                                   .where(id_server=guild.id, id_user=author.id, id_channel=channel.id).build)
                    row = cursor.fetchone()

                with self.cursor_context(commit=True) as cursor:
                    if not row:
                        cursor.execute(*db_util.insert("statistics_global")
                                       .items(id_server=guild.id, id_user=author.id,
                                              id_channel=channel.id, msg_count=1).build)
                    else:
                        row_id = row[0]
                        cursor.execute(*db_util.update("statistics_global").items(msg_count=DBFunction("msg_count+1"))
                                       .where(id=row_id).build)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with self.cursor_context(commit=True) as cursor:
            cursor.execute(*db_util.insert("event_logs")
                           .items(id_server=member.guild.id, id_user=member.id,
                                  date_utc=DBFunction("NOW()"), event_type="joined").build)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        with self.cursor_context(commit=True) as cursor:
            cursor.execute(*db_util.insert("event_logs")
                           .items(id_server=member.guild.id, id_user=member.id,
                                  date_utc=DBFunction("NOW()"), event_type="left").build)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        with self.cursor_context(commit=True) as cursor:
            cursor.execute(*db_util.insert("event_logs")
                           .items(id_server=guild.id, id_user=user.id,
                                  date_utc=DBFunction("NOW()"), event_type="banned").build)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        with self.cursor_context(commit=True) as cursor:
            cursor.execute(*db_util.insert("event_logs")
                           .items(id_server=guild.id, id_user=user.id,
                                  date_utc=DBFunction("NOW()"), event_type="banned").build)


def setup(bot):
    cog = Stats(bot)
    bot.add_cog(cog)
