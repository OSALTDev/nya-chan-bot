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
        bot_channel = self.bot.get_channel(332644650462478336)
        if bot_channel is None:
            await ctx.channel.send('The dedicated bot commands channel cannot be found')
            return False
        if ctx.invoked_subcommand is None:
            await bot_channel.send('Invalid Ask me Anything command passed, {}'.format(ctx.author.mention))

    @qna.command(description='')
    @commands.guild_only()
    @commands.has_any_role('Nixie', 'Supervisors', 'Moderators')
    async def validate(self, ctx):
        """Copy every question with your :upvote: reaction on it to the Question- channel"""
        bot_channel = self.bot.get_channel(332644650462478336)
        if bot_channel is None:
            await ctx.channel.send('The dedicated bot commands channel cannot be found')
            return False
        nb_copied = 0
        destination = self.bot.get_channel(331363194780254210)
        if destination is None:
            await bot_channel.send('There is no destination channel.')
            return False
        async for msg in ctx.channel.history(limit=200):
            to_copy = False
            for reaction in msg.reactions:
                from_me = False
                async for usr in reaction.users():
                    if usr.id == ctx.author.id:
                        from_me = True
                if reaction.emoji.name == 'upvote' and from_me is True:
                    to_copy = True
            if to_copy:
                nb_copied += 1
                await destination.send(
                    'From {} | {} UTC | (Processed by {})\n-----------------------\n{}'.format(msg.author.mention,
                                                                                               msg.created_at.strftime(
                                                                                                   '%c'),
                                                                                               ctx.author.mention,
                                                                                               msg.content))
                await msg.delete()
        await bot_channel.send('{} message(s) transferred to {}.'.format(nb_copied, destination.name))

    @qna.command(description='')
    @commands.guild_only()
    @commands.has_any_role('Nixie', 'Supervisors', 'Moderators')
    async def clean(self, ctx):
        """Delete every message with your :downvote: reaction"""
        bot_channel = self.bot.get_channel(332644650462478336)
        if bot_channel is None:
            await ctx.channel.send('The dedicated bot commands channel cannot be found')
            return False
        nb_deleted = 0
        async for msg in ctx.channel.history(limit=200):
            to_delete = False
            for reaction in msg.reactions:
                from_me = False
                async for usr in reaction.users():
                    if usr.id == ctx.author.id:
                        from_me = True
                if reaction.emoji.name == 'downvote' and from_me is True:
                    to_delete = True
            if to_delete:
                nb_deleted += 1
                await msg.delete()
        await bot_channel.send('{} message(s) have been removed in {}.'.format(nb_deleted, ctx.channel.mention))

    @qna.command(description='')
    @commands.guild_only()
    @commands.has_any_role('Nixie', 'Supervisors', 'Moderators')
    async def process(self, ctx, timestamp: str = None):
        """Process every question with your :upvote: reaction on it, save it to the database and remove it"""
        bot_channel = self.bot.get_channel(332644650462478336)
        if bot_channel is None:
            await ctx.channel.send('The dedicated bot commands channel cannot be found')
            return False
        connection = self.config.db_connection()
        cursor = connection.cursor()
        # Get the last stream ID
        cursor.execute("""SELECT id FROM streams WHERE id_server = %s ORDER BY `date` DESC LIMIT 1""", (ctx.guild.id))
        rows = cursor.fetchall()
        if len(rows) == 0:
            await bot_channel.send('No streams have been found !')
            return False
        stream_id = rows[0][0]
        nb_saved = 0
        destination = self.bot.get_channel(331363194780254210)
        if destination is None:
            await bot_channel.send('There is no destination channel.')
            return False
        async for msg in ctx.channel.history(limit=200):
            to_save = False
            for reaction in msg.reactions:
                from_me = False
                async for usr in reaction.users():
                    if usr.id == ctx.author.id:
                        from_me = True
                if reaction.emoji.name == 'upvote' and from_me is True:
                    to_save = True
            if to_save:
                question_details = msg.content.split('\n-----------------------\n')
                if len(question_details) != 2:
                    await bot_channel.send('question_details fail.')
                    continue
                question_infos = question_details[0].split(' | ')
                if len(question_infos) != 3:
                    await bot_channel.send('question_infos fail.')
                    continue
                nb_saved += 1
                q_content = question_details[1]
                q_author = question_infos[0].replace('From ', '')
                q_date = datetime.strptime(question_infos[1].replace(' UTC', ''), '%c')
                if timestamp is None:
                    q_timestamp = ''
                else:
                    q_timestamp = timestamp
                cursor.execute(
                    """INSERT INTO
                        questions (id, id_server, id_stream, author, datetime, question, timestamp)
                        VALUES (null, %s, %s, %s, %s, %s, %s)""",
                    (ctx.guild.id, stream_id, q_author, q_date.strftime('%Y-%m-%d %H:%M:%S'), q_content, q_timestamp))
                connection.commit()
                await msg.delete()
        await bot_channel.send('{} message(s) transferred to {}.'.format(nb_saved, destination.name))


def setup(bot):
    cog = Ama(bot)
    bot.add_cog(cog)
