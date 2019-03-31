import os
import subprocess
import discord
import psutil
import sys
from discord.ext import commands
from cogs.base_cog import BaseCog
from database import Methods as db_util


class Cog(BaseCog, name="Owner"):
    @commands.group(invoke_without_command=True)
    async def git(self, ctx):
        """Git commands."""
        await self.no_invoke_help(ctx)

    async def cog_check(self, ctx):
        if not await ctx.bot.is_owner(ctx.author):
            raise commands.NotOwner('You do not own this bot.')
        return True

    @git.command()
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
    async def branches(self, ctx):
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

    @commands.group(invoke_without_command=True)
    async def cogs(self, ctx):
        """Cogs related commands."""
        await self.no_invoke_help(ctx)

    @cogs.command()
    async def list(self, ctx):
        """Lists loaded cogs."""
        if not self.bot.extensions:
            await ctx.author.send("```No modules loaded```")
            return

        await ctx.author.send("```Loaded modules : {}```".format(", ".join(self.bot.extensions.keys())))

    @cogs.command()
    async def load(self, ctx, cog_name: str):
        """Loads a cog."""
        # try:
        if f"cogs.{cog_name}" not in self.bot.extensions:
            try:
                self.bot.load_extension('cogs.' + cog_name)
            except (AttributeError, ImportError) as e:
                print("Failed to load cog: {} due to {}".format(cog_name, str(e)))
                await ctx.author.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            else:
                await ctx.author.send("```{} loaded.```".format(cog_name))
        else:
            await ctx.author.send("```py\n'{}' module is already loaded\n```".format(cog_name))

    @cogs.command()
    async def unload(self, ctx, cog_name: str):
        """Unloads a cog."""
        if f"cogs.{cog_name}" in self.bot.extensions:
            try:
                self.bot.unload_extension('cogs.' + cog_name)
            except (AttributeError, ImportError) as e:
                print("Failed to unload cog: {} due to {}".format(cog_name, str(e)))
                await ctx.author.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            else:
                await ctx.author.send("```{} unloaded.```".format(cog_name))
        else:
            await ctx.author.send("```py\n'{}' module is not loaded\n```".format(cog_name))

    @cogs.command()
    async def reload(self, ctx, cog_name: str):
        """Reloads a cog."""
        if cog_name in self.bot.extensions:
            try:
                self.bot.unload_extension('cogs.' + cog_name)
                self.bot.load_extension('cogs.' + cog_name)
            except (AttributeError, ImportError) as e:
                print("Failed to unload cog: {} due to {}".format(cog_name, str(e)))
                await ctx.author.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            else:
                await ctx.author.send("```{} reloaded.```".format(cog_name))
        else:
            await ctx.author.send("```py\n'{}' module is not loaded\n```".format(cog_name))

    @commands.command()
    @commands.guild_only()
    async def say(self, ctx, channel: discord.TextChannel, *, msg):
        """Says something as Nya."""
        await channel.send(" ".join(str(x) for x in msg))

    @commands.command()
    async def status(self, ctx, *, game_name):
        """Sets the now playing message."""
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name=game_name, type=0))

    @commands.command()
    @commands.guild_only()
    async def role_ids(self, ctx):
        role_list = [
            '{} - {}'.format(role.name, role.id)
            for role in ctx.guild.roles
        ]
        await ctx.author.send('{}'.format("\n".join(role_list)))

    @commands.command()
    @commands.guild_only()
    async def chan_ids(self, ctx):
        chan_list = [
            '{} - {}'.format(chan.name, chan.id)
            for chan in ctx.guild.channels
        ]
        await ctx.author.send('{}'.format("\n".join(chan_list)))

    @commands.command()
    async def shutdown(self, ctx):
        """Shutdown bot."""
        await self.bot.logout()

    @commands.command()
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

    @commands.command()
    async def name(self, ctx):
        with self.cursor_context(commit=True) as cursor:
            cursor.execute(*db_util.select("event_logs").items("id_user")
                           .where(id_server=325197025719091201).distinct.build)
            rows = cursor.fetchall()

        if rows:
            with self.cursor_context(commit=True) as cursor:
                for row in rows:
                    user = await self.bot.get_user_info(row[0])
                    if user is None:
                        continue

                    cursor.execute(*db_util.insert("users", id_user=user.id, user_name=str(user)))
        await ctx.author.send('Done')
