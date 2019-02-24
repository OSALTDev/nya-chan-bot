from discord.ext import commands
from discord.ext.commands import group
from cogs.base_cog import BaseCog
import discord
from nyalib.NyaBot import ThrowawayException
from NyaChan import before_invoke_event as setup_reply


class Tags(BaseCog, name="Tags"):
    def __init__(self, bot):
        super().__init__(bot)
        self.on_msg_dict = {
            "+": {
                "pre": {
                    bool(1): "You already", bool(0): "You now"
                }
            },
            "-": {
                "pre": {
                    bool(1): "You no longer", bool(0): "You don\'t"
                }
            },
            "method": lambda message, has_role: getattr(message.author, "remove_roles" if has_role else "add_roles")
        }

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.content[:1] not in '+-' or \
                message.channel.id != self.bot.config.bot.channel.bot_commands:
            return

        sign = message.content[:1]
        specified_tag = message.content[1:]
        if specified_tag == "":
            return

        # Check if tag exists in database
        with self.cursor_context() as cursor:
            cursor.execute("""SELECT name, channel FROM tags WHERE id_server = %s AND name=%s LIMIT 1""",
                           (message.guild.id, specified_tag))
            row = cursor.fetchone()

        if not row:
            await message.channel.send(
                'The tag **{}** does not exist, {}.'.format(specified_tag, message.author.mention))
            return

        tag_name = row[0]
        tag_role = discord.utils.get(message.guild.roles, name=tag_name)
        if tag_role is None:
            tag_role = await message.guild.create_role(name=tag_name, mentionable=False, reason="Tag creation")

        has_role = discord.utils.get(message.author.roles, id=tag_role.id) is not None
        msg_str = self.on_msg_dict[sign]

        await message.channel.send(
            '{} have the **{}** tag, {}.'.format(msg_str["pre"][has_role], tag_role.name, message.author.mention))

        if (has_role and sign == "-") or (not has_role and sign == "+"):
            callback = self.on_msg_dict["method"](message, has_role)
            await callback(tag_role)

    async def cog_before_invoke(self, ctx):
        await setup_reply(ctx)
        if ctx.invoked_subcommand is not None:
            tag = ctx.kwargs.get("tag")

            # Check if tag exists in database
            with self.cursor_context() as cursor:
                cursor.execute("""SELECT name, channel FROM tags WHERE id_server = %s AND name=%s LIMIT 1""",
                               (ctx.guild.id, tag))
                row = cursor.fetchone()

            if not row:
                await ctx.reply('The tag "{}" does not exist, {}'.format(tag, ctx.author.mention))
                raise ThrowawayException

            tag_name = row[0]
            channel_id = row[1]

            # Check if the role associated with the tag exists, if not, create it
            tag_role = discord.utils.get(ctx.guild.roles, name=tag_name)
            if tag_role is None:
                tag_role = await ctx.guild.create_role(name=tag_name, mentionable=True, reason="Tag creation")

            # Get the linked channel if applicable
            channel = self.bot.get_channel(channel_id) if channel_id else None

            # Check if the author already has tag_role
            has_role = discord.utils.get(ctx.author.roles, id=tag_role.id) is not None

            ctx.linked_channel = channel
            ctx.tag_role = tag_role
            ctx.has_role = has_role

    @group()
    async def tag(self, ctx):
        """Tag commands."""
        if ctx.invoked_subcommand is None:
            await ctx.reply('Invalid tag command passed, {}'.format(ctx.author.mention))

    @tag.command(description='Identify yourself with a tag. Let other people know about you.')
    @commands.guild_only()
    async def add(self, ctx, *, tag: str):
        """Identify yourself with a tag."""
        if ctx.has_role:
            await ctx.reply('You already have the tag "{}"'.format(ctx.tag_role.name))
            return

        await ctx.author.add_roles(ctx.tag_role)

        msg = 'You now have the tag "{}"'.format(ctx.tag_role.name)
        if ctx.linked_channel is not None:
            msg += '. You can now see the channel {}'.format(ctx.linked_channel.mention)

        await ctx.reply(msg)

    @tag.command(description='Removes with a tag.')
    @commands.guild_only()
    async def remove(self, ctx, *, tag: str):
        """Removes a tag."""
        if not ctx.has_role:
            await ctx.reply('You don\'t have the tag "{}"'.format(ctx.tag_role.name))
            return

        await ctx.author.remove_roles(ctx.tag_role)

        msg = 'You no longer have the tag "{}"'.format(ctx.tag_role.name)
        if ctx.linked_channel is not None:
            msg += '. The channel {} is now hidden'.format(ctx.linked_channel.mention)

        await ctx.reply(msg)

    @commands.command(description='Lists the available tags.')
    @commands.guild_only()
    async def tags(self, ctx):
        """Lists the available tags"""
        with self.cursor_context() as cursor:
            cursor.execute("""SELECT name, description, channel FROM tags WHERE id_server = %s ORDER BY name ASC""",
                           ctx.guild.id)
            rows = cursor.fetchall()

        embed = discord.Embed(title="List of the available tags", type="rich",
                              colour=discord.Colour.from_rgb(0, 174, 134),
                              description="You can add those tags to your profile by using the command **+tag** :"
                                          "```\nExample: +Gamer```or remove them by using the command **-tag** :"
                                          "```\nExample: -Gamer```\n**These commands only work in #bot-commands **\n\n"
                                          "Role list:")
        for row in rows:
            value = row[1]

            channel = self.bot.get_channel(row[2]) if row[2] else None
            if channel is not None:
                value += ' (Make {} visible)'.format(channel.mention)

            embed.add_field(name=row[0], value=value, inline=False)

        if not embed.fields:
            embed.add_field(name="None defined", value="No roles have been defined for self-assignment")

        await ctx.reply(embed=embed)


def setup(bot):
    cog = Tags(bot)
    bot.add_cog(cog)
