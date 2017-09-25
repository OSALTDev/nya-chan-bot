import discord
from discord.ext import commands
from discord.ext.commands import group
from cogs.base_cog import BaseCog


class Channels(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)

    # @group()
    # async def ch(self, ctx):
    #     """Channel edition commands."""
    #     bot_channel = self.bot.get_channel(333753806644969472)
    #     if bot_channel is None:
    #         await ctx.channel.send('The dedicated bot commands channel cannot be found')
    #         return False
    #     if ctx.invoked_subcommand is None:
    #         await bot_channel.send('Invalid Channel Edition command passed, {}'.format(ctx.author.mention))

    @group()
    async def tch(self, ctx):
        """Text Channel edition commands."""
        if ctx.invoked_subcommand is None:
            await self.bot_reply(ctx, 'Invalid Text Channel Edition command passed, {}'.format(ctx.author.mention))

    @tch.command(description='Create a new text channel with Supervisor permission.')
    @commands.has_any_role('Nixie', 'Supervisors')
    @commands.guild_only()
    async def create(self, ctx, *channel_name):
        """Create a new text channel with Supervisor permission."""
        guild = ctx.guild
        channel_name = " ".join(channel_name)
        for channel in guild.text_channels:
            if channel.name == channel_name:
                await self.bot_reply(ctx, 'Channel **{}** already exists, {}'.format(channel_name, ctx.author.mention))
                return False
        supervisor_role = None
        for role in guild.roles:
            if role.name == 'Supervisors':
                supervisor_role = role
                break
        if supervisor_role is None:
            return False
        perms = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            supervisor_role: discord.PermissionOverwrite(read_messages=True, manage_roles=True)
        }
        await guild.create_text_channel(channel_name, overwrites=perms)

        #     @ch.command(description='Create a new temporary game channel.')
        #     @commands.guild_only()
        #     async def game(self, ctx):
        #         """Create new game channel, must specify a name"""
        #         bot_channel = self.bot.get_channel(333753806644969472)
        #         if bot_channel is None:
        #             await ctx.channel.send('The dedicated bot commands channel cannot be found')
        #             return False
        #         main_game_channel = self.bot.get_channel(335240794145554432)
        #         if main_game_channel is None:
        #             await bot_channel.send('The main Games channel cannot be found')
        #             return False
        #         # First check that the original Games channel is not empty
        #         if len(main_game_channel.members) == 0:
        #             await ctx.author.send('The main Games channel is empty at the moment, please use it.')
        #             return False
        #         # Check the temporary game channels
        #         tmp_voice_channels = []
        #         available_tmp_channels = []
        #         next_channel_number = 2
        #         for tmp_game_chan in ctx.guild.voice_channels:
        #             if tmp_game_chan.name.startswith('Gaming Room '):
        #                 tmp_voice_channels.append(tmp_game_chan)
        #                 next_channel_number += 1
        #                 if len(tmp_game_chan.members) == 0:
        #                     available_tmp_channels.append(tmp_game_chan)
        #         if len(available_tmp_channels) > 0:
        #             await ctx.author.send('The following Game Rooms are empty, please use one of them : {}.'.format(
        #                 ", ".join(chan.name for chan in available_tmp_channels)))
        #             return False
        #         next_channel_position = main_game_channel.position + 1
        #         if len(tmp_voice_channels) > 0:
        #             next_channel_position = tmp_voice_channels[-1].position + 1
        #         # Create a new Game room
        #         new_game_room = await ctx.guild.create_voice_channel('Gaming Room {}'.format(next_channel_number))
        #         await asyncio.sleep(2)
        #         await new_game_room.edit(position=next_channel_position)
        #         await ctx.author.send(
        #             'The channel {} has just been created, feel free to join !\
        # Every empty **Game Room** are removed every hours.'.format(new_game_room.name))

        # async def garbage_collector(self, bot_channel):
        #     next_channel_number = 2
        #     for tmp_game_chan in bot_channel.guild.voice_channels:
        #         if not tmp_game_chan.name.startswith('Gaming Room '):
        #             continue
        #         if len(tmp_game_chan.members) == 0:
        #             await bot_channel.send('**{}** has been deleted for inactivity.'.format(tmp_game_chan.name))
        #             await tmp_game_chan.delete()
        #         else:
        #             await tmp_game_chan.edit(name='Gaming Room {}'.format(next_channel_number))
        #             next_channel_number += 1
        #     await asyncio.sleep(30)
        #     await self.garbage_collector(bot_channel)
        #
        # async def on_ready(self):
        #     bot_channel = self.bot.get_channel(333753806644969472)
        #     await self.garbage_collector(bot_channel)


def setup(bot):
    cog = Channels(bot)
    # bot.add_listener(cog.on_ready, "on_ready")
    bot.add_cog(cog)
