import discord
import contextlib


class BaseCog(object):
    def __init__(self, bot):
        self.bot = bot
        self.config = self.bot.config
        self.bot_channel = None
        # TODO: add logger here.

    @contextlib.contextmanager
    def cursor_context(self, commit=False, connection_yield=False):
        connection = self.config.db_connection()
        cursor = connection.cursor()
        if connection_yield:
            yield cursor, connection
        else:
            yield cursor
        if commit:
            connection.commit()
        connection.close()
