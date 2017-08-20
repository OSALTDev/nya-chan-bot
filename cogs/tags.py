from discord.ext import commands
from discord.ext.commands import group
from cogs.base_cog import BaseCog
import discord


class Tags(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)

    async def member_message(self, message):
        if message.author.bot:
            return False
        if message.channel.name != "bot-commands":
            return False
        if not message.content.startswith('+') and not message.content.startswith('-'):
            return False
        sign = message.content[:1]
        specified_tag = message.content[1:]
        # Check if tag exists in database
        connection = self.config.db_connection()
        cursor = connection.cursor()
        if specified_tag == "":
            return False
        cursor.execute("""SELECT name, channel FROM tags WHERE id_server = %s AND name=%s LIMIT 1""",
                       (message.guild.id, specified_tag))
        rows = cursor.fetchall()
        connection.close()
        if len(rows) == 0:
            await message.channel.send(
                'The tag **{}** does not exist, {}.'.format(specified_tag, message.author.mention))
            return False
        tag_name = rows[0][0]
        tag_role = None
        for role in message.guild.roles:
            if role.name == tag_name:
                tag_role = role
                break
        if tag_role is None:
            tag_role = await message.guild.create_role(name=tag_name, mentionable=False, reason="Tag creation")
        has_role = False
        for member_role in message.author.roles:
            if member_role.id == tag_role.id:
                has_role = True
                break
        if sign == '+':
            if has_role is True:
                await message.channel.send(
                    'You already have the **{}** tag, {}.'.format(tag_role.name, message.author.mention))
            else:
                await message.author.add_roles(tag_role)
                await message.channel.send(
                    'You now have the **{}** tag, {}.'.format(tag_role.name, message.author.mention))
        elif sign == '-':
            if has_role is True:
                await message.author.remove_roles(tag_role)
                await message.channel.send(
                    'You no longer have the **{}** tag, {}.'.format(tag_role.name, message.author.mention))
            else:
                await message.channel.send(
                    'You don\'t have the **{}** tag, {}.'.format(tag_role.name, message.author.mention))

    @group()
    async def tag(self, ctx):
        """Tag commands."""
        bot_channel = self.bot.get_channel(332644650462478336)
        if bot_channel is None:
            await ctx.channel.send('The dedicated bot commands channel cannot be found')
            return False
        if ctx.invoked_subcommand is None:
            await bot_channel.send('Invalid tag command passed, {}'.format(ctx.author.mention))

    @tag.command(description='Identify yourself with a tag. Let other people know about you.')
    @commands.guild_only()
    async def add(self, ctx, *tag: str):
        """Identify yourself with a tag."""
        bot_channel = self.bot.get_channel(332644650462478336)
        if bot_channel is None:
            await ctx.channel.send('The dedicated bot commands channel cannot be found')
            return False
        tag = " ".join(str(x) for x in tag)
        # Check if tag exists in database
        connection = self.config.db_connection()
        cursor = connection.cursor()
        cursor.execute("""SELECT name, channel FROM tags WHERE id_server = %s AND name=%s LIMIT 1""",
                       (ctx.guild.id, tag))
        rows = cursor.fetchall()
        connection.close()
        if len(rows) == 0:
            await bot_channel.send('The tag "{}" does not exist, {}'.format(tag, ctx.author.mention))
            return False
        tag_name = rows[0][0]
        # Check if the role associated with the tag exists, if not, create it
        tag_role = None
        for role in ctx.guild.roles:
            if role.name == tag_name:
                tag_role = role
        if tag_role is None:
            tag_role = await ctx.guild.create_role(name=tag_name, mentionable=True, reason="Tag creation")
        # Get the linked channel if applicable
        channel = None
        if not rows[0][1] == 'None':
            channel = self.bot.get_channel(int(rows[0][1]))
        # Check if the author already has tag_role
        has_role = False
        for role in ctx.author.roles:
            if role.id == tag_role.id:
                has_role = True
                break
        if has_role:
            await bot_channel.send('You already have the tag "{}", {}'.format(tag_name, ctx.author.mention))
            return False
        await ctx.author.add_roles(tag_role)
        msg = 'You now have the tag "{}", {}'.format(tag_name, ctx.author.mention)
        if channel is not None:
            msg += '. You can now see the channel {}'.format(channel.mention)
        await bot_channel.send(msg)

    @tag.command(description='Removes with a tag.')
    @commands.guild_only()
    async def remove(self, ctx, *tag: str):
        """Removes a tag."""
        bot_channel = self.bot.get_channel(332644650462478336)
        if bot_channel is None:
            await ctx.channel.send('The dedicated bot commands channel cannot be found')
            return False
        tag = " ".join(str(x) for x in tag)
        # Check if tag exists in database
        connection = self.config.db_connection()
        cursor = connection.cursor()
        cursor.execute("""SELECT name, channel FROM tags WHERE id_server = %s AND name=%s LIMIT 1""",
                       (ctx.guild.id, tag))
        rows = cursor.fetchall()
        connection.close()
        if len(rows) == 0:
            await bot_channel.send('The tag "{}" does not exist, {}'.format(tag, ctx.author.mention))
            return False
        tag_name = rows[0][0]
        # Check if the role associated with the tag exists, if not, create it
        tag_role = None
        for role in ctx.guild.roles:
            if role.name == tag_name:
                tag_role = role
        if tag_role is None:
            tag_role = await ctx.guild.create_role(name=tag_name, mentionable=True, reason="Tag creation")
        # Get the linked channel if applicable
        channel = None
        if not rows[0][1] == 'None':
            channel = self.bot.get_channel(int(rows[0][1]))
        # Check if the author already has tag_role
        has_role = False
        for role in ctx.author.roles:
            if role.id == tag_role.id:
                has_role = True
                break
        if not has_role:
            await bot_channel.send('You don\'t have the tag "{}", {}'.format(tag_name, ctx.author.mention))
            return False
        await ctx.author.remove_roles(tag_role)
        msg = 'You no longer have the tag "{}", {}'.format(tag_name, ctx.author.mention)
        if channel is not None:
            msg += '. The channel {} is now hidden'.format(channel.mention)
        await bot_channel.send(msg)

    @commands.command(description='Lists the available tags.')
    @commands.guild_only()
    async def tags(self, ctx):
        """Lists the available tags"""
        connection = self.config.db_connection()
        cursor = connection.cursor()
        cursor.execute("""SELECT name, description, channel FROM tags WHERE id_server = %s ORDER BY name ASC""",
                       ctx.guild.id)
        rows = cursor.fetchall()
        connection.close()
        embed = discord.Embed(title="List of the available tags", type="rich",
                              colour=discord.Colour.from_rgb(0, 174, 134),
                              description="You can add those tags to your profile by using the command **+tag** :\
```\nExample: +Gamer```or remove them by using the command **-tag** :\
```\nExample: -Gamer```\n**These commands only work in #bot-commands **\n")
        for row in rows:
            value = row[1]
            if not row[2] == 'None':
                channel = self.bot.get_channel(int(row[2]))
                if channel is not None:
                    value = value + ' (Make {} visible)'.format(channel.mention)
            embed.add_field(name=row[0], value=value, inline=False)
        await self.bot_reply(ctx, '', embed=embed)


def setup(bot):
    cog = Tags(bot)
    bot.add_listener(cog.member_message, "on_message")
    bot.add_cog(cog)
