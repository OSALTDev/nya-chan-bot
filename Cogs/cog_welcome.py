from discord.ext import commands
import mysql.connector
import role_ids
from __main__ import config

class Welcome():
    def __init__(self, bot):
        self.bot = bot

    @bot.event
    async def on_member_join(member):
        guild = member.guild
        conn = mysql.connector.connect(host=config['Database']['host'],user=config['Database']['user'],password=config['Database']['password'], database=config['Database']['database'])
        cursor = conn.cursor()
        cursor.execute("""SELECT message FROM welcomes WHERE id_server = %s""", (member.guild.id))
        rows = cursor.fetchall()
        conn.close()
        text = rows[0][0]
        try:
            await member.send(text.format(member, guild))
        except:
            pass

def setup(bot):
    bot.add_cog(Misc(bot))

