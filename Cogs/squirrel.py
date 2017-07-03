from discord.ext import commands
import asyncio
import datetime
import role_ids
import sys, os

class Squirrel():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Add a user to the Squirrel Army.')
    @commands.guild_only()
    @commands.has_any_role('Nixie', 'Mods', 'Elder Squirrel')
    async def squirreladd(self, ctx, username: str):
        """Add a user to the Squirrel Army"""
        squirrel_role = None
        for x in ctx.guild.roles:
            if x.id == 331563592560410634:  #329409494478094336
                squirrel_role = x
        if squirrel_role == None:
            await ctx.channel.send('There is no Squirrel Army role on this server.')
            return False
        try:
            converter = commands.converter.MemberConverter()
            future_squirrel = converter.convert(ctx, username)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno, str(e))        
        #if future_squirrel is None:
        #    await ctx.channel.send('The user {} cannot be found'.format(username))
        #    return False;
        #future_squirrel.add_roles(squirrel_role)
        #squirrel_channel = self.bot.get_channel(325420488107098112)
        #if squirrel_channel is None:
        #    await ctx.channel.send('The Squirrel Army channel cannot be found')
        #    return False;
        #await squirrel_channel.send('Welcome in the Squirrel Army {}, happy squirreling =^.^='.format(future_squirrel.mention))

def setup(bot):
    cog = Squirrel(bot)
    bot.add_cog(cog)
