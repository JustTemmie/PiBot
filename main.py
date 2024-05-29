import discord
from discord.ext import commands
from discord import app_commands

import logging
import logging.handlers

from datetime import datetime
import time

import json
import asyncio
import glob
import os

import libraries.APIs.config as configLib 


config = configLib.getConfig()
settings = configLib.getSettings()

directories_to_make = ["local_only"]
directories_to_empty = ["temp", "logs"]

for dir in directories_to_make + directories_to_empty:
    if not os.path.exists(dir):
        os.mkdir(dir)
        
if config["DEVELOPMENT"]:
    for dir in directories_to_empty:
        for file in os.listdir(dir):
            os.remove(f"{dir}/{file}")

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='logs/discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.config = config
        self.settings = settings
        
        self.ready = False
        
        super().__init__(
            command_prefix="q",
            intents=discord.Intents.all(),
            owner_ids=self.config["OWNER_IDS"],
        *args, **kwargs)

        # self.tree = app_commands.CommandTree(self)
        self.start_time = datetime.now()
        

    async def on_ready(self) -> None:
        print(f"Succesfully logged in as {self.user}")
        self.ready = True

    async def setup_hook(self) -> None:
        async def sync_tree(self):
            print(f"Syncing command tree...")
            if self.config["DEVELOPMENT"]:
                guild = discord.Object(id=config["DEVELOPMENT_GUILD"])
                self.tree.copy_global_to(guild=guild)
                await self.tree.sync()
            else:
                await self.tree.sync()
            print(f"Command tree synced!")
            
        if self.config["SYNC_TREE"]:
            await sync_tree(self)
        else:
            print("miku is set to not sync tree, continuing")
    

bot = Bot()
# miku.tree = discord.app_commands.CommandTree(miku)
# miku.remove_command("help")



async def main():
    async with bot:
        for filename in glob.iglob("./cogs/**", recursive=True):
            if filename.endswith(".py"):
                # goes from "./cogs/economy.py" to "cogs.economy"
                filename = filename[2:].replace("/", ".")[:-3]
                await bot.load_extension(filename)
    
        await bot.start(bot.config["API_KEYS"]["DISCORD"])


bot.loop = asyncio.new_event_loop()
asyncio.set_event_loop(bot.loop)
asyncio.run(main())
