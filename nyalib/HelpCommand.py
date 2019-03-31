import discord
from discord.ext.commands import DefaultHelpCommand
import itertools


class Command(DefaultHelpCommand):
    async def add_indented_commands(self, commands, *, heading=None, max_size=None, size=None):
        if not commands:
            return

        if not size:
            size = 1

        if heading:
            self.paginator.add_line(heading)
        max_size = max_size or self.get_max_size(commands)

        get_width = discord.utils._string_width
        for command in commands:
            name = command.name
            width = max_size - (get_width(name) - len(name))
            entry = '{0}{1:<{width}} {2}'.format(self.indent * ' ' * size, name, command.short_doc, width=width)
            self.paginator.add_line(self.shorten_text(entry))

            if isinstance(command, discord.ext.commands.Group) and self.context.bot.config.bot.subcommands_in_help:
                size += 1
                cmds = []
                for c in command.commands:
                    try:
                        await c.can_run(self.context)
                    except discord.ext.commands.errors.CheckFailure:
                        continue

                    cmds.append(c)

                await self.add_indented_commands(cmds, max_size=max_size, size=size)
                size -= 1

    async def send_pages(self):
        """A helper utility to send the page output from :attr:`paginator` to the destination."""
        destination = self.get_destination()
        for page in self.paginator.pages:
            try:
                await destination.send(page)
            except discord.Forbidden:
                await self.context.reply(page)

    async def send_bot_help(self, mapping):
        ctx = self.context
        bot = ctx.bot

        if bot.description:
            # <description> portion
            self.paginator.add_line(bot.description, empty=True)

        no_category = '\u200b{0.no_category}:'.format(self)
        def get_category(command, *, no_category=no_category):
            cog = command.cog
            return cog.qualified_name + ':' if cog is not None else no_category

        filtered = await self.filter_commands(bot.commands, sort=True, key=get_category)
        max_size = self.get_max_size(filtered)
        to_iterate = itertools.groupby(filtered, key=get_category)

        # Now we can add the commands to the page.
        for category, commands in to_iterate:
            commands = sorted(commands, key=lambda c: c.name) if self.sort_commands else list(commands)
            await self.add_indented_commands(commands, heading=category, max_size=max_size)

        note = self.get_ending_note()
        if note:
            self.paginator.add_line()
            self.paginator.add_line(note)

        await self.send_pages()

    async def send_command_help(self, command):
        self.add_command_formatting(command)
        self.paginator.close_page()
        await self.send_pages()

    async def send_group_help(self, group):
        self.add_command_formatting(group)

        filtered = await self.filter_commands(group.commands, sort=self.sort_commands)
        await self.add_indented_commands(filtered, heading=self.commands_heading)

        if filtered:
            note = self.get_ending_note()
            if note:
                self.paginator.add_line()
                self.paginator.add_line(note)

        await self.send_pages()

    async def send_cog_help(self, cog):
        if cog.description:
            self.paginator.add_line(cog.description, empty=True)

        filtered = await self.filter_commands(cog.get_commands(), sort=self.sort_commands)
        await self.add_indented_commands(filtered, heading=self.commands_heading)

        note = self.get_ending_note()
        if note:
            self.paginator.add_line()
            self.paginator.add_line(note)

        await self.send_pages()
