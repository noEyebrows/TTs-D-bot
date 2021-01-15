import os
import asyncio
import discord
import logging
import asyncpg
import ast
import random
from collections import deque
from tempfile import TemporaryFile
from discord.ext.commands import has_permissions, MissingPermissions
from gtts import gTTS
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


bot = discord.ext.commands.Bot(command_prefix='-')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

bot.run(TOKEN)
