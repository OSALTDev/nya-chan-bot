from discord.ext import commands
import distro, subprocess
from cogs.base_cog import BaseCog


class Cog(BaseCog, name="Server"):
    @commands.command(description='Pat Nya Chan.')
    @commands.has_any_role('Nixie', 'Supervisors', 'Moderators')
    @commands.guild_only()
    async def serverstats(self, ctx):
        """Get server stats"""
        os_info = distro.linux_distribution(full_distribution_name=False)
        uptime_days = int(round(float(subprocess.getoutput("cat /proc/uptime").split()[0]) / 86400))
        loadavg = subprocess.getoutput("cat /proc/loadavg").split()
        ram_usage = subprocess.getoutput("free -m")
        disk_usage = subprocess.getoutput("df -h")
        listening_stats = subprocess.getoutput("netstat -l | grep -P '(\*:|\[::]:)'")
        active_connections_v4 = subprocess.getoutput(
            "netstat -Wn --numeric-ports -a -4 | grep -v LISTEN | tail -n +3 | "
            "awk '{print $4}' | cut -d':' -f1 | uniq -c | sort -r "
        )

        msg = (
            "OS: {} {} ({})".format(os_info[0], os_info[1], os_info[2]),
            "System Uptime: {} days".format(str(uptime_days)),
            "Load Averages: {} {} {}".format(loadavg[0], loadavg[1], loadavg[2]),
            "RAM usage:\n\n{}".format(ram_usage),
            "Disk Usage:\n\n{}".format(disk_usage),
            "Servers Listening:\n\n{}".format(listening_stats),
            "Active Connections (v4):\n\n{}".format(active_connections_v4)
        )
        await ctx.channel.send("\n\n".join(msg))
