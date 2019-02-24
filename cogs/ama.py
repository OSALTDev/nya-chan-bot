import discord
from discord.ext import commands
from discord.ext.commands import group
from datetime import datetime
from cogs.base_cog import BaseCog


class Ama(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)

    @group()
    async def qna(self, ctx):
        """Ask me Anything commands."""
        if ctx.invoked_subcommand is None:
            await ctx.reply('Invalid Ask me Anything command passed, {}'.format(ctx.author.mention))

    @qna.command(description='')
    @commands.guild_only()
    @commands.has_any_role('Nixie', 'Supervisors', 'Moderators')
    async def validate(self, ctx):
        """Copy every question with your :upvote: reaction on it to the Question- channel"""
        copied = []
        destination = self.bot.get_channel(331363194780254210)
        if destination is None:
            await ctx.reply('There is no destination channel.')
            return

        async for msg in ctx.channel.history(limit=200):
            to_copy = False
            for reaction in msg.reactions:
                if reaction.emoji.name == 'upvote':
                    from_me = discord.utils.get(reaction.users().flatten(), id=ctx.author.id) is not None
                    to_copy = from_me
                    break

            if to_copy:
                copied.append(msg)
                await destination.send(
                    (
                        'From {} | {} UTC | (Processed by {})\n'
                        '-----------------------\n'
                        '{}'
                    ).format(msg.author.mention, msg.created_at.strftime('%c'),
                             ctx.author.mention, msg.content)
                )

        if copied:
            for msg in copied:
                await msg.delete()

        await ctx.reply('{} message(s) transferred to {}.'.format(len(copied), destination.name))

    @qna.command(description='')
    @commands.guild_only()
    @commands.has_any_role('Nixie', 'Supervisors', 'Moderators')
    async def clean(self, ctx):
        """Delete every message with your :downvote: reaction"""
        deleted = []
        async for msg in ctx.channel.history(limit=200):
            to_delete = False
            for reaction in msg.reactions:
                if reaction.emoji.name == 'downvote':
                    from_me = discord.utils.get(reaction.users().flatten(), id=ctx.author.id) is not None
                    to_delete = from_me
                    break

            if to_delete:
                deleted.append(msg)

        if deleted:
            for msg in deleted:
                await msg.delete()

        await ctx.reply('{} message(s) have been removed in {}.'.format(len(deleted), ctx.channel.mention))

    @qna.command(description='')
    @commands.guild_only()
    @commands.has_any_role('Nixie', 'Supervisors', 'Moderators')
    async def process(self, ctx, timestamp: str = None):
        """Process every question with your :upvote: reaction on it, save it to the database and remove it"""
        saved = []
        with self.cursor_context() as cursor:
            # Get the last stream ID
            res = cursor.execute("""SELECT id FROM streams WHERE id_server = %s ORDER BY `date` DESC LIMIT 1""", (ctx.guild.id))
            if not res:
                await ctx.reply('No streams have been found !')
                return

            row = cursor.fetchone()

        stream_id = row[0]
        destination = self.bot.get_channel(331363194780254210)
        if destination is None:
            await ctx.reply('There is no destination channel.')
            return

        async for msg in ctx.channel.history(limit=200):
            to_save = False
            for reaction in msg.reactions:
                if reaction.emoji.name == 'upvote':
                    from_me = discord.utils.get(reaction.users().flatten(), id=ctx.author.id) is not None
                    to_save = from_me
                    break

            if to_save:
                question_details = msg.content.split('\n-----------------------\n')
                if len(question_details) != 2:
                    await ctx.reply('question_details fail.')
                    continue

                question_infos = question_details[0].split(' | ')
                if len(question_infos) != 3:
                    await ctx.reply('question_infos fail.')
                    continue

                saved.append(msg)
                q_content = question_details[1]
                q_author = question_infos[0].replace('From ', '')
                q_date = datetime.strptime(question_infos[1].replace(' UTC', ''), '%c')
                q_timestamp = '' if timestamp is None else timestamp

                with self.cursor_context(commit=True) as cursor:
                    cursor.execute(
                        "INSERT INTO questions (id, id_server, id_stream, author, datetime, question, timestamp)"
                        "VALUES (null, %s, %s, %s, %s, %s, %s)",
                        (
                            ctx.guild.id, stream_id, q_author,
                            q_date.strftime('%Y-%m-%d %H:%M:%S'), q_content, q_timestamp
                        )
                    )

        if saved:
            for msg in saved:
                await msg.delete()

        await ctx.reply('{} message(s) transferred to {}.'.format(len(saved), destination.name))


def setup(bot):
    cog = Ama(bot)
    bot.add_cog(cog)
