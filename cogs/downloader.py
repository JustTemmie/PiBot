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
        @commands.is_owner()
        async def download_context_command(interaction: discord.Integration, message: discord.Message) -> None:
            if len(message.attachments) == 0:
                await interaction.response.send_message("This message doesn't have any attachments", ephemeral=True)
                return
            
            await interaction.response.send_message(f"Oki :3 - downloading {len(message.attachments)} attachment(s)", ephemeral=True)
            
            folders = {
                "images": ["png", "svg", "jpeg", "jpg", "webp"],
                "gifs": ["gif", "gifv"],
                "videos": ["mp4", "webm", "mvk", "avi", "m4v", "3gp", "mxf", "mov"],
                "audio": ["ogg", "mp3", "wav", "3gp", "opus", "oga"],
                "misc": []
            }

            for folder in folders:
                media_folder = self.bot.config["FOLDER_PATHS"]["VIDEOS"] + folder
                if not os.path.exists(media_folder):
                    os.mkdir(media_folder)
            
            for attatchment in message.attachments:
                
                filename = attatchment.filename
                folder = f"{list(folders.keys())[-1]}/"
                prefix = ""
                new_filename = ""
                
                for folder in folders:
                    for file_type in folders[folder]:
                        if filename.endswith(file_type):
                            folder = f"{folder}/"
                            break
                    
                    else:
                        continue
                    break
                
                while True:
                    if prefix == "":
                        new_filename = self.bot.config["FOLDER_PATHS"]["VIDEOS"] + folder + attatchment.filename
                    else:
                        new_filename = self.bot.config["FOLDER_PATHS"]["VIDEOS"] + folder + f"(copy {prefix}) - " + attatchment.filename
                    
                    if os.path.isfile(new_filename):
                        if prefix == "":
                            prefix = 0
                        prefix += 1
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