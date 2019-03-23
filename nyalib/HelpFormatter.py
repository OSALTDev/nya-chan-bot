import discord
from discord.ext.commands import HelpFormatter, Paginator, Command
import itertools
import inspect


class Formatter(HelpFormatter):
    async def _add_subcommands_to_page(self, max_width, commands, size=None):
        if not size:
            size = 1
        for name, command in commands:
            if name in command.aliases:
                # skip aliases
                continue
            width_gap = discord.utils._string_width(name) - len(name)

            entry = '  ' * size + '{0:<{width}} {1}'.format(name, command.short_doc, width=max_width-width_gap)
            shortened = self.shorten(entry)
            self._paginator.add_line(shortened)

            if isinstance(command, discord.ext.commands.Group) and self.context.bot.config.bot.subcommands_in_help:
                size += 1
                cmds = [
                    (c.name, c)
                    for c in command.commands
                    if await c.can_run(self.context)
                ]
                await self._add_subcommands_to_page(max_width, cmds, size)
                size -= 1

    async def format(self):
        """Handles the actual behaviour involved with formatting.

        To change the behaviour, this method should be overridden.

        Returns
        --------
        list
            A paginated output of the help command.
        """
        self._paginator = Paginator()

        # we need a padding of ~80 or so

        description = self.command.description if not self.is_cog() else inspect.getdoc(self.command)

        if description:
            # <description> portion
            self._paginator.add_line(description, empty=True)

        if isinstance(self.command, Command):
            # <signature portion>
            signature = self.get_command_signature()
            self._paginator.add_line(signature, empty=True)

            # <long doc> section
            if self.command.help:
                self._paginator.add_line(self.command.help, empty=True)

            # end it here if it's just a regular command
            if not self.has_subcommands():
                self._paginator.close_page()
                return self._paginator.pages

        max_width = self.max_name_size + 2

        def category(tup):
            cog = tup[1].cog_name
            # we insert the zero width space there to give it approximate
            # last place sorting position.
            return cog + ':' if cog is not None else '\u200b' + self.no_category + ':'

        filtered = await self.filter_command_list()
        data = sorted(filtered, key=category)
        for category, commands in itertools.groupby(data, key=category):
            # there simply is no prettier way of doing this.
            commands = sorted(commands)
            if len(commands) > 0:
                self._paginator.add_line(category)

            await self._add_subcommands_to_page(max_width, commands)

        # add the ending note
        self._paginator.add_line()
        ending_note = self.get_ending_note()
        self._paginator.add_line(ending_note)
        return self._paginator.pages
