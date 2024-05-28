import discord
from discord.ext import commands
from discord import app_commands

import platform
import psutil
import subprocess
import time
from datetime import datetime

import libraries.helpers as helpers

class PurgeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        @bot.tree.command(name="purge")
        @app_commands.allowed_installs(guilds=False, users=True) # users only, no guilds for install
        @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True) # all allowed
        @commands.is_owner()
        async def purge_command(interaction: discord.Interaction, amount: int) -> None:
            await interaction.response.send_message(f"purged {amount} messages", ephemeral=True)
            
            while amount > 0:
                await interaction.channel.purge(limit = min(amount, 100))
                amount -= 100
            


async def setup(bot):
    await bot.add_cog(PurgeCog(bot))
