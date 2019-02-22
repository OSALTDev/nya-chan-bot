import discord
import contextlib


class BaseCog(object):
    def __init__(self, bot):
        self.bot = bot
        self.config = self.bot.config
        self.bot_channel = None
        # TODO: add logger here.

    @contextlib.contextmanager
    def cursor_context(self):
        connection = self.config.db_connection()
        cursor = connection.cursor()
        yield cursor
        connection.commit()
        connection.close()

    async def bot_reply(self, ctx, content, tts=False, embed=None, file=None, files=None, reason=None,
                        delete_after=None, nonce=None):
        # Send a bot reply to the appropriate channel
        # - If command issued in DM, reply in DM
        # - If command issued in bot-command, reply in bot-command
        # - If command issued elsewhere, reply in DM, if that fails, reply in bot-command,
        #   if not found reply in same channel
        # TODO: Disable commands outside of bot-commands
        if ctx.guild is None:
            self.bot_channel = ctx.author
        elif ctx.channel.name == "bot-commands":
            self.bot_channel = ctx.channel
        else:
            try:
                await ctx.author.send(content=content, tts=tts, embed=embed, file=file, files=files, reason=reason,
                                      delete_after=delete_after, nonce=nonce)
                return False
            except discord.Forbidden:
                self.bot_channel = discord.utils.get(ctx.guild.channels, name="bot-commands")
                if self.bot_channel is None:
                    self.bot_channel = ctx.channel

        await self.bot_channel.send(content=content, tts=tts, embed=embed, file=file, files=files, reason=reason,
                                    delete_after=delete_after, nonce=nonce)
