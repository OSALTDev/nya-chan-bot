from cogs.base_cog import BaseCog
import contextlib


class Stats(BaseCog):
    """Keep track of the amount of messages everyone send"""

    def __init__(self, bot):
        super().__init__(bot)

    @contextlib.contextmanager
    def cursor_context(self):
        connection = self.config.db_connection()
        cursor = connection.cursor()
        yield cursor
        connection.commit()
        connection.close()

    async def on_message(self, message):
        if not message.content.startswith(self.bot.command_prefix) and not message.author.bot:
            guild = message.guild
            author = message.author
            channel = message.channel
            if channel is not None:
                with self.cursor_context() as cursor:
                    cursor.execute(
                        """SELECT id FROM statistics_global 
                        WHERE id_server = %s AND id_user = %s AND id_channel = %s""",
                        (guild.id, author.id, channel.id))
                    rows = cursor.fetchall()
                    if len(rows) == 0:
                        cursor.execute(
                            """INSERT INTO statistics_global (id, id_server, id_user, id_channel, msg_count) 
                            VALUES (null, %s, %s, %s, 1)""",
                            (guild.id, author.id, channel.id)
                        )
                    else:
                        row_id = rows[0][0]
                        cursor.execute(
                            """UPDATE statistics_global SET msg_count = msg_count + 1 
                            WHERE id = %s""", (row_id)
                        )

    async def on_member_join(self, member):
        with self.cursor_context() as cursor:
            cursor.execute(
                """INSERT INTO event_logs (id, id_server, id_user, date_utc, event_type) 
                VALUES (null, %s, %s, NOW(), "joined")""",
                (member.guild.id, member.id))

    async def on_member_remove(self, member):
        with self.cursor_context() as cursor:
            cursor.execute(
                """INSERT INTO event_logs (id, id_server, id_user, date_utc, event_type) 
                VALUES (null, %s, %s, NOW(), "left")""",
                (member.guild.id, member.id))

    async def on_member_ban(self, guild, user):
        with self.cursor_context() as cursor:
            cursor.execute(
                """INSERT INTO event_logs (id, id_server, id_user, date_utc, event_type) 
                VALUES (null, %s, %s, NOW(), "banned")""",
                (guild.id, user.id))

    async def on_member_unban(self, guild, user):
        with self.cursor_context() as cursor:
            cursor.execute(
                """INSERT INTO event_logs (id, id_server, id_user, date_utc, event_type) 
                VALUES (null, %s, %s, NOW(), "unbanned")""",
                (guild.id, user.id))


def setup(bot):
    cog = Stats(bot)
    bot.add_cog(cog)
