from .base_cog import BaseCog
from discord.ext import commands
from database import Methods as db_util
from database import DBFunction


class Cog(BaseCog, name="DBEvent"):
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.content.startswith(self.bot.command_prefix) and not message.author.bot:
            guild = message.guild
            author = message.author
            channel = message.channel
            if guild is not None:
                with self.cursor_context() as cursor:
                    db_util.select("statistics_global").items("id", "msg_count").where(
                        id_server=guild.id, id_user=author.id, id_channel=channel.id
                    ).run(cursor)
                    row = cursor.fetchone()

                with self.cursor_context(commit=True) as cursor:
                    if not row:
                        db_util.insert("statistics_global").items(
                            id_server=guild.id, id_user=author.id,
                            id_channel=channel.id, msg_count=1
                        ).run(cursor)
                    else:
                        row_id = row[0]
                        db_util.update("statistics_global").items(
                            msg_count=DBFunction("msg_count+1")
                        ).where(id=row_id).run(cursor)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with self.cursor_context(commit=True) as cursor:
            db_util.insert("event_logs").items(
                id_server=member.guild.id, id_user=member.id,
                date_utc=DBFunction("NOW()"), event_type="joined"
            ).run(cursor)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        with self.cursor_context(commit=True) as cursor:
            db_util.insert("event_logs").items(
                id_server=member.guild.id, id_user=member.id,
                date_utc=DBFunction("NOW()"), event_type="left"
            ).run(cursor)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        with self.cursor_context(commit=True) as cursor:
            db_util.insert("event_logs").items(
                id_server=guild.id, id_user=user.id,
                date_utc=DBFunction("NOW()"), event_type="banned"
            ).run(cursor)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        with self.cursor_context(commit=True) as cursor:
            db_util.insert("event_logs").items(
                id_server=guild.id, id_user=user.id,
                date_utc=DBFunction("NOW()"), event_type="left"
            ).run(cursor)
