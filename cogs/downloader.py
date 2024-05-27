import discord
from discord.ext import commands
from discord import app_commands

import os
import aiohttp
import random

class DownloaderCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        
        @bot.tree.context_menu(name="Save Attachments")
        @app_commands.user_install()
        @discord.is_owner()
        async def download_context_command(interaction: discord.Integration, message: discord.Message) -> None:
            if len(message.attachments) == 0:
                await interaction.response.send_message("This message doesn't have any attachments", ephemeral=True)
                return
            
            await interaction.response.send_message(f"Oki :3 - downloading {len(message.attachments)} attachment(s)", ephemeral=True)
            
            for attatchment in message.attachments:
                
                suffix = ""
                new_filename = ""
                while True:
                    new_filename = self.bot.config["FOLDER_PATHS"]["VIDEOS"] + attatchment.filename + str(suffix)
                    if os.path.isfile(new_filename):
                        if suffix == "":
                            suffix = 0
                        suffix += 1
                    else:
                        break
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(attatchment.url) as data:
                        with open(new_filename, "wb") as f:
                            while True:
                                chunk = await data.content.read()
                                if not chunk:
                                    break
                                f.write(chunk)

async def setup(bot):
    await bot.add_cog(DownloaderCog(bot))