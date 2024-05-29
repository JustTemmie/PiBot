import discord
from discord.ext import commands
from discord import app_commands

import platform
import psutil
import subprocess
import time
from datetime import datetime
import requests
import json

from bs4 import BeautifulSoup
from pdf2image import convert_from_path


import libraries.helpers as helpers

class PfpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        @bot.tree.command(name="pfp")
        @app_commands.allowed_installs(guilds=False, users=True)
        @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
        async def pfp_command_register(interaction: discord.Interaction, user: discord.User = None, ephemreal: bool = True) -> None:
            await self.pfp_command(interaction, user, ephemreal)
            
    async def pfp_command(self, interaction: discord.Interaction, user: discord.User, ephemreal: bool):
        if not user:
            user = interaction.user

        av_button = discord.ui.Button(label="Open External", url=user.display_avatar.url, emoji="📩")
        view = discord.ui.View()
        view.add_item(av_button)

        embed = discord.Embed()
        embed.set_image(url=user.display_avatar.url)
        embed.color = user.colour

        await interaction.response.send_message(embed=embed, view=view, ephemeral=ephemreal)


async def setup(bot):
    await bot.add_cog(PfpCog(bot))
