import discord
from discord.ext import commands
import pymysql
import role_ids
from __main__ import config

class Welcome():
    """Welcomes new members to the server via private message"""
    def __init__(self, bot):
        self.bot = bot

    def get_message(self, member):
        guild = member.guild
        connection = pymysql.connect(host=config['Database']['host'], user=config['Database']['user'], password=config['Database']['password'], db=config['Database']['database'], charset='utf8')
        cursor = connection.cursor()
        cursor.execute("""SELECT message FROM welcomes WHERE id_server = %s""", (guild.id))
        rows = cursor.fetchall()
        connection.close()
        text = rows[0][0]
        return text.format(member, guild)

    async def member_join(self, member):
        text = self.get_message(member)
        try:
            await member.send(text)
        except:
            pass

    @commands.command(description='Send the welcome message via private message again.')
    @commands.guild_only()
    async def welcome(self, ctx):
        """Resend welcome message"""
        member = ctx.message.author
        text = self.get_message(member)
        try:
            await member.send(text)
        except:
            pass

def setup(bot):
    cog = Welcome(bot)
    bot.add_listener(cog.member_join, "on_member_join")
    bot.add_cog(cog)

