from discord.ext import commands
from cogs.base_cog import BaseCog
import discord
import time


class Cog(BaseCog, name="Customs"):
    """Welcomes new members to the server via private message"""
    @commands.command(description='Sends a custom message.')
    @commands.guild_only()
    async def cc(self, ctx, command_name: str):
        """Sends a custom message"""
        with self.cursor_context() as cursor:
            cursor.execute("""SELECT `message` FROM `custom_commands` WHERE `id_server` = %s AND `command` = %s""",
                           (ctx.guild.id, command_name))
            row = cursor.fetchone()

        if not row:
            await ctx.reply('The custom message **{}** doesn\'t exist, {}'.format(command_name, ctx.author.mention))
            return

        text = row[0]
        await ctx.channel.send(text)

    @commands.command(description='Explain the kicks.')
    @commands.guild_only()
    async def accident(self, ctx):
        """Explain the kicks"""
        embed = discord.Embed(title="Announcement Regarding Accidental Kicking",
                              url='https://www.youtube.com/watch?v=I9GcnRAdY2M')
        embed.set_thumbnail(url='https://i.ytimg.com/vi/I9GcnRAdY2M/maxresdefault.jpg')
        embed.add_field(name="▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬",
                        value="**Joker here, with an announcement for all my lovely adoring fans here at "
                              "Joker Asylum!**\n\n**You may have noticed we had some regulars having to rejoin "
                              "this server, having been kicked!**\n\n**I just gotta say, ya don't know what it's "
                              "like to really be kicked till you've had Bane's foot on your back...or maybe his knee! "
                              "Baaaaaahahahaha!**\n\n**I'm only joking! Honestly, Bats really should learn to watch "
                              "his back... Nyaaaaahahahahahaha.**",
                        inline=True)
        embed.set_footer(
            text="For real though, we just want to sincerely apologize for anyone who may have accidentally "
                 "been kicked. We were checking some member info in the member listings, specifically regarding "
                 "activity, and unfortunately that info is listed in the same window as the \"prune\" function. "
                 "A mis-click occurred and *quite* a few of you were boop'd. We all know tech derps sometimes "
                 "happen, but we want to once more sincerely apologize and hope no one was offended or hurt by it.")
        await ctx.channel.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    @commands.guild_only()
    async def kicked(self, ctx):
        with self.cursor_context(commit=True) as cursor:
            cursor.execute("""SELECT DISTINCT `id_user` FROM `statistics_global`""")
            member_ids = cursor.fetchall()
            nb_kicked = 0
            for member_id in member_ids:
                member = ctx.guild.get_member(int(member_id[0]))
                if member is None:
                    cursor.execute("""INSERT INTO `kicked` (`id`, `id_user`) VALUES (NULL, %s)""", member_id[0])
                    nb_kicked += 1

        await ctx.author.send('{} Users were kicked'.format(nb_kicked))

    @commands.command()
    @commands.is_owner()
    @commands.guild_only()
    async def safeguard(self, ctx):
        # Get "User" role
        user_role = discord.utils.get(ctx.guild.roles, name="Users")
        if user_role is None:
            await ctx.author.send("There is no Users role !")
            return

        nb_user = 0
        nb_bot = 0
        nb_has_role = 0
        message = await ctx.send("Starting to add the **Users** role to everyone (max 100 members)...")

        start = time.time()
        for member in ctx.guild.members:
            if member.bot:
                nb_bot += 1
                continue

            has_role = discord.utils.get(member.roles, name="Users") is not None
            if has_role is True:
                nb_has_role += 1
                continue

            await member.add_roles(user_role, reason="Safeguard against pruning.")

            nb_user += 1
            if nb_user == 100:
                break
        end = time.time()

        seconds = end - start
        await message.delete()
        await ctx.send(
            (
                "**{}** / **{}** Members were added to the role **Users** in {} seconds.\n"
                "Bots skipped : **{}**\nMembers who already had the role : **{}**"
            ).format(nb_user, len(ctx.guild.members), round(seconds, 3), nb_bot, nb_has_role))
