import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import aiohttp


load_dotenv() # Loads .env file
token = os.getenv('TOKEN') # Gets Token from .env file
guild = discord.Object(os.getenv('GUILD_ID'))


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix='j?', intents=intents)

@client.event
async def on_ready():
    print(f"The bot is running as {client.user} (ID: {client.user.id})")
    synced = await client.tree.sync(guild=guild)
    print(f"Synced {len(synced)} commands to guild {guild.id}")

@client.tree.command(name="ping", description="Displays the bot latency", guild=guild)
async def ping(interaction: discord.Interaction) -> None:
    embed  = discord.Embed(
        title="🏓 Pong!",
        description=f"The bot latency is {round(client.latency * 1000)}ms.",
        color=0x103DDE
    )
    await interaction.response.send_message(embed=embed) 

@client.tree.command(name="randomfact", description="Gives you a random fact", guild=guild)
async def randomfact(interaction: discord.Interaction) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get("https://uselessfacts.jsph.pl/random.json?language=en") as request:
            if request.status == 200:
                data = await request.json()
                embed = discord.Embed(description=data["text"], color=0x103DDE)
            else:
                embed = discord.Embed(
                    title="Error!",
                    description="There is something wrong with the API, please try again later",
                    color=0xE02B2B
                )
            await interaction.response.send_message(embed=embed)

client.run(token)