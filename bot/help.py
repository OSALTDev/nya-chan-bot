from discord.ext.commands import DefaultHelpCommand


class NyaHelp(DefaultHelpCommand):
    def add_command_formatting(self, command):
        if command.description:
            self.paginator.add_line(command.description, empty=True)

        signature = self.get_command_signature(command)
        self.paginator.add_line(signature, empty=True)

        if command.help:
            try:
                self.paginator.add_line(command.help.format(prefix=self.context.prefix), empty=True)
            except RuntimeError:
                for line in command.help.splitlines():
                    self.paginator.add_line(line)
                self.paginator.add_line()

    def disabled_command(self, command):
        permissions_cog = self.context.bot.get_cog("Permissions")
        guild_config = permissions_cog.db.find(guild_id=str(self.context.guild.id))
        return "disabled_commands" in guild_config.getStore() and \
               command.qualified_name in guild_config["disabled_commands"]

    async def send_command_help(self, command):
        if self.disabled_command(command):
            return False

        await super().send_command_help(command)

    async def send_group_help(self, group):
        if self.disabled_command(group):
            return False

        await super().send_group_help(group)
