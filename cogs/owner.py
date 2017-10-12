import os
import subprocess
import discord
import psutil
import sys
from discord.ext import commands
from discord.ext.commands import command
from discord.ext.commands import group
from cogs.base_cog import BaseCog


class Owner(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)

    @group()
    async def git(self, ctx):
        """Git commands."""
        if ctx.invoked_subcommand is None:
            await ctx.author.send('Invalid git command passed, {}'.format(ctx.author.mention))

    @git.command()
    @commands.is_owner()
    async def update(self, ctx, args='default'):
        """Updates bot."""
        try:
            branch = self.config.git_branch if args == 'default' else args
            # Retrieving latest code from upstream.
            process1 = subprocess.check_output("git fetch".format(branch), stderr=subprocess.STDOUT,
                                               shell=True)
            process = subprocess.check_output("git checkout origin/{}".format(branch), stderr=subprocess.STDOUT,
                                              shell=True)
            await ctx.author.send("```Git pull from '{}' success```".format(branch))
        except Exception as e:
            await ctx.author.send("```py\nError while git pulling\n```")
            raise commands.UserInputError(ctx)

    @git.command()
    @commands.is_owner()
    async def branches(self, ctx, args='default'):
        """Lists branches."""

        try:
            from git import Repo
            repo = Repo(os.path.join(os.getcwd(), ".git"))
            remotes = repo.remotes[0].refs

            for item in remotes:
                await ctx.author.send(item.remote_head)

        except Exception as e:
            await ctx.author.send("```py\nError listing git branches\n```")
            raise commands.UserInputError(ctx)

    @group()
    async def cogs(self, ctx):
        """Cogs related commands."""
        if ctx.invoked_subcommand is None:
            await ctx.author.send('Invalid cogs command passed, {}'.format(ctx.author.mention))

    @cogs.command()
    @commands.is_owner()
    async def list(self, ctx):
        """Lists loaded cogs."""
        if len(self.bot.loaded_cogs) > 0:
            await ctx.author.send("```Loaded modules : {}```".format(", ".join(self.bot.loaded_cogs)))
        else:
            await ctx.author.send("```No module loaded```")

    @cogs.command()
    @commands.is_owner()
    async def load(self, ctx, cog_name: str):
        """Loads a cog."""
        # try:
        if cog_name not in self.bot.loaded_cogs:
            try:
                self.bot.load_cog(cog_name)
                await ctx.author.send("```{} loaded.```".format(cog_name))
            except (AttributeError, ImportError) as e:
                await ctx.author.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        else:
            await ctx.author.send("```py\n'{}' module is already loaded\n```".format(cog_name))

    @cogs.command()
    @commands.is_owner()
    async def unload(self, ctx, cog_name: str):
        """Unloads a cog."""
        if cog_name in self.bot.loaded_cogs:
            self.bot.unload_cog(cog_name)
            await ctx.author.send("```{} unloaded.```".format(cog_name))
        else:
            await ctx.author.send("```py\n'{}' module is not loaded\n```".format(cog_name))

    @cogs.command()
    @commands.is_owner()
    async def reload(self, ctx, cog_name: str):
        """Reloads a cog."""
        if cog_name in self.bot.loaded_cogs:
            self.bot.reload_cog(cog_name)
            await ctx.author.send("```{} reloaded.```".format(cog_name))
        else:
            await ctx.author.send("```py\n'{}' module is not loaded\n```".format(cog_name))

    @command()
    @commands.is_owner()
    @commands.guild_only()
    async def say(self, ctx, channel_name: str, *msg):
        """Says something as Nya."""
        channel = None
        for chan in ctx.guild.channels:
            if chan.name == channel_name:
                channel = chan

        if channel is not None:
            await channel.send(" ".join(str(x) for x in msg))
        else:
            await ctx.author.send("```py\n'{}' channel has not been found\n```".format(channel_name))
            raise commands.UserInputError(ctx, 'Channel not found')

    @command()
    @commands.is_owner()
    async def nowplaying(self, ctx, *game_name):
        """Sets the now playing message."""
        await self.bot.change_presence(game=discord.Game(name=" ".join(str(x) for x in game_name), type=0))

    @command()
    @commands.is_owner()
    @commands.guild_only()
    async def role_ids(self, ctx):
        role_list = []
        for role in ctx.guild.roles:
            role_list.append('{} - {}'.format(role.name, role.id))
        await ctx.author.send('{}'.format("\n".join(str(x) for x in role_list)))

    @command()
    @commands.is_owner()
    @commands.guild_only()
    async def chan_ids(self, ctx):
        chan_list = []
        for chan in ctx.guild.channels:
            chan_list.append('{} - {}'.format(chan.name, chan.id))
        await ctx.author.send('{}'.format("\n".join(str(x) for x in chan_list)))

    @command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Shutdown bot."""
        await self.bot.logout()

    @command()
    @commands.is_owner()
    async def restart(self, ctx):
        """Restarts bot."""
        try:
            p = psutil.Process(os.getpid())
            for handler in p.get_open_files() + p.connections():
                os.close(handler.fd)
        except Exception as e:
            pass
        python = sys.executable
        os.execl(python, python, *sys.argv)

    @command()
    @commands.is_owner()
    async def name(self, ctx):
        connection = self.config.db_connection()
        cursor = connection.cursor()
        cursor.execute("""SELECT DISTINCT id_user FROM event_logs WHERE id_server = %s""", 325197025719091201)
        rows = cursor.fetchall()
        for row in rows:
            user = await self.bot.get_user_info(row[0])
            if user is None:
                continue
            username = "{}#{}".format(user.name, user.discriminator)
            cursor.execute("""INSERT INTO users (id, id_user, user_name) VALUES (null, %s, %s)""", (user.id, username))
            connection.commit()
        connection.close()
        await ctx.author.send('Done')


def setup(bot):
    cog = Owner(bot)
    bot.add_cog(cog)
