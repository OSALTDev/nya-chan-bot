import discord
from discord.ext import commands
import pymysql
import role_ids
from __main__ import config

class Customs():
    """Welcomes new members to the server via private message"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Sends a custom message.')
    @commands.guild_only()
    async def cc(self, ctx, command_name : str):
        """Sends a custom message"""
        connection = pymysql.connect(host=config['Database']['host'], user=config['Database']['user'], password=config['Database']['password'], db=config['Database']['database'], charset='utf8')
        cursor = connection.cursor()
        cursor.execute("""SELECT `message` FROM `custom_commands` WHERE `id_server` = %s AND `command` = %s""", (guild.id, command_name))
        rows = cursor.fetchall()
        connection.close()
        if len(rows) > 0:
            text = rows[0][0]
            return text.format(member, guild)

def setup(bot):
    cog = Customs(bot)
    bot.add_cog(cog)

