from discord.ext import commands
import asyncio
import datetime
import pymysql
import role_ids
from __main__ import config

class Ama():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='')
    @commands.guild_only()
    async def copyq(self, ctx):
        """Copy every question with your :upvote: reaction on it to the Question- channel"""
        nb_copied = 0
        destination = self.bot.get_channel(331363194780254210)
        if destination is None:
            await ctx.channel.send('There is no destination channel.')
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
                await destination.send('From {} | {} UTC | (Processed by {})\n-----------------------\n{}'.format(msg.author.mention, msg.created_at.strftime('%c'), ctx.author.mention, msg.content))
                await msg.delete()
        await ctx.channel.send('{} message(s) transferred to {}.'.format(nb_copied, destination.name))
                    
                      
        
    @commands.command(description='')
    @commands.guild_only()
    async def cleanq(self, ctx):
        """Delete every message with your :downvote: reaction"""
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
        await ctx.channel.send('{} message(s) have been processed.'.format(nb_deleted))

    @commands.command(description='')
    @commands.guild_only()
    async def processq(self, ctx, timestamp : str = None):
        """Process every question with your :upvote: reaction on it, save it to the database and remove it"""
        connection = pymysql.connect(host=config['Database']['host'], user=config['Database']['user'], password=config['Database']['password'], db=config['Database']['database'], charset='utf8')
        cursor = connection.cursor()
        #Get the last stream ID
        cursor.execute("""SELECT id FROM streams WHERE id_server = %s ORDER BY `date` DESC LIMIT 1""", (ctx.guild.id))
        rows = cursor.fetchall()
        if len(rows) == 0:
            await ctx.channel.send('No streams have been found !')
            return False
        stream_id = row[0][0]
        nb_saved = 0
        destination = self.bot.get_channel(331363194780254210)
        if destination is None:
            await ctx.channel.send('There is no destination channel.')
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
                question_details = msg.content.split('\n--------------------------\n')
                if len(question_details) != 2:
                    continue
                question_infos = question_details[0].split(' | ')
                if len(question_infos) != 3:
                    continue
                nb_saved += 1
                q_content = question_details[1]
                q_author = question_infos[0].replace('From ', '')
                q_date = question_infos[1].replace(' UTC', '')       
                if timestamp is None:
                    q_timestamp = ''
                else:
                    q_timestamp = timestamp
                cursor.execute("""INSERT INTO messages (id, id_server, id_stream, author, datetime, question, timestamp) VALUES (null, %s, %s, %s, %s, %s, %s)""", (guild.id, id_stream, q_author, q_date, q_content, q_timestamp))
                connection.commit()
                #await destination.send('From {} - {} UTC (Processed by {})\n--------------------------\n{}'.format(msg.author.mention, msg.created_at.strftime('%c'), ctx.author.mention, msg.content))
                #await msg.delete()
        await ctx.channel.send('{} message(s) transferred to {}.'.format(nb_saved, destination.name))

def setup(bot):
    cog = Ama(bot)
    bot.add_cog(cog)
