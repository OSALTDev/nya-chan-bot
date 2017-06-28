import discord
from discord.ext import commands
import pymysql
import role_ids
from __main__ import config

class Welcome():
    def __init__(self, bot):
        self.bot = bot

    async def member_join(self, member):
        guild = member.guild
        connection = pymysql.connect(host=config['Database']['host'], user=config['Database']['user'], password=config['Database']['password'], db=config['Database']['database'], charset='utf8')
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO welcomes (id_server, message) VALUES(%s, %s)""", (guild.id, 'coucou'))
        #cursor.execute("""SELECT message FROM welcomes WHERE id_server = %s""", (member.guild.id))
        #rows = cursor.fetchall()
        connection.commit()
        connection.close()
        #text = rows[0][0]
        #try:
            #await member.send(text.format(member, guild))
        #except:
            #pass

def setup(bot):
    cog = Welcome(bot)
    bot.add_listener(cog.member_join, "on_member_join")
    bot.add_cog(cog)

