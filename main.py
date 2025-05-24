import discord
import os
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"The bot is running as {client.user}")

load_dotenv()
token = os.getenv("TOKEN")
client.run(token)