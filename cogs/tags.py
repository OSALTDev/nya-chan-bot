from discord.ext import commands
from cogs.base_cog import BaseCog
import discord


class Tags(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.command(description='Identify yourself with a tag. Let other people know about you.')
    @commands.guild_only()
    async def tag(self, ctx, tag: str):
        """Identify yourself with a tag."""
        # Check if tag exists in database
        connection = self.config.db_connection()
        cursor = connection.cursor()
        cursor.execute("""SELECT name FROM tags WHERE id_server = %s AND name=%s""", (ctx.guild.id, tag))
        rows = cursor.fetchall()
        connection.close()
        if len(rows) == 0:
            await ctx.channel.send('The tag "{}" does not exist, {}'.format(tag, ctx.author.mention))
            return False
        tag_name = rows[0][0]
        # Check if the role associated with the tag exists, if not, create it
        tag_role = None
        for role in ctx.guild.roles:
            if role.name == tag_name:
                tag_role = role
        if tag_role is None:
            tag_role = await ctx.guild.create_role(name=tag_name, colour=discord.Colour.from_rgb(147, 23, 17),
                                                   mentionable=True, reason="Tag creation")
        # Check if the author already has tag_role
        has_role = False
        for role in ctx.author.roles:
            if role.id == tag_role.id:
                has_role = True
                break
        if has_role:
            await ctx.author.remove_roles(tag_role)
            await ctx.channel.send('You no longer have the tag "{}", {}'.format(tag_name, ctx.author.mention))
        else:
            await ctx.author.add_roles(tag_role)
            await ctx.channel.send('You now have the tag "{}", {}'.format(tag_name, ctx.author.mention))

    @commands.command(description='Identify yourself with a tag. Let other people know about you.')
    @commands.guild_only()
    async def tags(self, ctx):
        """List the available tags"""
        connection = self.config.db_connection()
        cursor = connection.cursor()
        cursor.execute("""SELECT name, description, channel FROM tags WHERE id_server = %s ORDER BY name ASC""", ctx.guild.id)
        rows = cursor.fetchall()
        connection.close()
        embed = discord.Embed(title="List of the available tags", type="rich",
                              colour=discord.Colour.from_rgb(0, 174, 134),
                              description="You can add those tags to your profile by using the command **!n.tag** :\
                                          ```\nExample: !n.tag Gamer```")
        for row in rows:
            value = row[1]
            if not row[2] == 'None':
                channel = await self.bot.get_channel(int(row[2]))
                if channel is not None:
                    value = value + ' (Give access to {})'.format(channel.mention)
            embed.add_field(name=row[0], value=row[1], inline=False)
        await ctx.channel.send(embed=embed)


def setup(bot):
    cog = Tags(bot)
    bot.add_cog(cog)
