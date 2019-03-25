import os
import subprocess
import discord
import psutil
import sys
import traceback
from discord.ext import commands
from cogs.base_cog import BaseCog
from database import Methods as db_util


class Cog(BaseCog, name="Owner"):
    @commands.group(invoke_without_command=True)
    async def git(self, ctx):
        """Git commands."""
        await ctx.send_help("git")

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
            await ctx.reply.dm("```Git pull from '{}' success```".format(branch))
        except Exception as e:
            await ctx.reply.dm("```py\nError while git pulling\n```")
            raise commands.UserInputError(ctx)

    @git.command()
    async def branches(self, ctx):
        """Lists branches."""

        try:
            from git import Repo
            repo = Repo(os.path.join(os.getcwd(), ".git"))
            remotes = repo.remotes[0].refs

            for item in remotes:
                await ctx.reply.dm(item.remote_head)

        except Exception as e:
            await ctx.reply.dm("```py\nError listing git branches\n```")
            raise commands.UserInputError(ctx)

    @commands.group(invoke_without_command=True)
    async def cogs(self, ctx):
        """Cogs related commands."""
        await ctx.send_help("cogs")

    @cogs.command()
    async def list(self, ctx):
        """Lists loaded cogs."""
        if not self.bot.extensions:
            await ctx.reply.dm("```No modules loaded```")
            return

        await ctx.reply.dm("```Loaded modules : {}```".format(", ".join(self.bot.extensions.keys())))

    @cogs.command()
    async def load(self, ctx, cog_name: str):
        """Loads a cog."""
        # try:
        try:
            self.bot.load_extension('cogs.' + cog_name)
        except commands.ExtensionAlreadyLoaded:
            await ctx.reply.dm(f"The cog `{cog_name}` is already loaded.")
        except commands.ExtensionNotFound:
            await ctx.reply.dm(f"The cog `{cog_name}` was not found.")
        except commands.NoEntryPointError:
            await ctx.reply.dm(f"The cog `{cog_name}` has no entry point method (setup or Cog.setup).")
        except commands.ExtensionFailed:
            await ctx.reply.dm(f"The cog `{cog_name}` was not loaded. Please check logs.")
            print(f"Failed to reload cog: {cog_name}")
            traceback.print_exc()
        else:
            await ctx.reply.dm(f"The cog `{cog_name}` has been loaded")

    @cogs.command()
    async def unload(self, ctx, cog_name: str):
        """Unloads a cog."""
        try:
            self.bot.unload_extension('cogs.' + cog_name)
        except commands.ExtensionNotLoaded:
            await ctx.reply.dm(f"The cog `{cog_name}` is not loaded.")
        else:
            await ctx.reply.dm(f"The cog `{cog_name}` has been unloaded")

    @cogs.command()
    async def reload(self, ctx, cog_name: str):
        """Reloads a cog."""
        try:
            self.bot.reload_extension('cogs.' + cog_name)
        except commands.ExtensionNotLoaded:
            await ctx.reply.dm(f"The cog `{cog_name}` is not loaded.")
        except commands.ExtensionNotFound:
            await ctx.reply.dm(f"The cog `{cog_name}` was not found.")
        except commands.NoEntryPointError:
            await ctx.reply.dm(f"The cog `{cog_name}` has no entry point method (setup or Cog.setup).")
        except commands.ExtensionFailed:
            await ctx.reply.dm(f"The cog `{cog_name}` was not loaded. Please check logs.")
            print(f"Failed to reload cog: {cog_name}")
            traceback.print_exc()
        else:
            await ctx.reply.dm(f"The cog `{cog_name}` has been reloaded")

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
        await ctx.reply.dm('{}'.format("\n".join(role_list)))

    @commands.command()
    @commands.guild_only()
    async def chan_ids(self, ctx):
        chan_list = [
            '{} - {}'.format(chan.name, chan.id)
            for chan in ctx.guild.channels
        ]
        await ctx.reply.dm('{}'.format("\n".join(chan_list)))

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
        await ctx.reply.dm('Done')
