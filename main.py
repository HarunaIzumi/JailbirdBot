import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv


load_dotenv() # Loads .env file
token = os.getenv('TOKEN') # Gets Token from .env file

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix='j?', intents=intents)

@client.event
async def on_ready():
    print(f"The bot is running as {client.user} (ID: {client.user.id})")

client.run(token)