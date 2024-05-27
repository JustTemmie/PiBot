import discord
from discord.ext import commands
from discord import app_commands

import platform
import psutil
import subprocess
import time
from datetime import datetime

import libraries.helpers as helpers

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()
        self.uname = platform.uname()

        
        @bot.tree.command(name="server-info")
        @app_commands.allowed_installs(guilds=False, users=True) # users only, no guilds for install
        @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True) # all allowed
        @commands.is_owner()
        async def info_command(interaction: discord.Interaction) -> None:
            embed = discord.Embed()
            embed.colour = discord.Colour.red()

            embed.title = "Server info"
            embed.description = f"some information regarding {self.bot.user.name}'s physical server"
            
            page_data = await self.get_info(1)
            for i in page_data:
                embed.add_field(
                    name=i,
                    value=page_data[i],
                    inline=False
                )
            
            await interaction.response.send_message(embed=embed)
            

    async def get_info(self, page):        
        if page == 1:
            cpu_frequency = psutil.cpu_freq()
            if cpu_frequency != None:
                self.max_cpu_frequency = round(cpu_frequency.max / 1000, 2)
            else:
                self.max_cpu_frequency = "?"
            
            return {
                "System": f"{self.uname.system} {self.uname.release}",
                "Processor": f"{platform.machine()} CPU with {psutil.cpu_count()} threads, clocked at {self.max_cpu_frequency} GHz",
                "Memory": f"using {round(psutil.virtual_memory().used / 1024**2)}/{round(psutil.virtual_memory().total / 1024**2)} MB",
                "System Uptime": helpers.format_time(round(time.time() - psutil.boot_time())),
                "Bot Uptime": helpers.format_time(round(time.time() - self.start_time)),
                "Ping": f"{round(self.bot.latency * 1000)}ms",
                "Python": f"version {platform.python_version()}",
                "Discord.py": f"version {discord.__version__}"
            }
        
        elif page == 2:
            return {
                "processor": psutil.cpu_freq(),
            }
            
        else:
            return {}


async def setup(bot):
    await bot.add_cog(Info(bot))
