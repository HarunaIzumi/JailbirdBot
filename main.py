from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
import logging

load_dotenv() #Loads enviroment variables
token = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

bot = commands.Bot(command_prefix="?", intents=intents, log_handler=handler)

@bot.event
async def on_ready():
    print(f"The bot is running as {bot.user}")

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def info(ctx):
    embed = discord.Embed(
        description = "This is the info page for **Nerissa's Little Jailbird** bot, created by <@156500926880940032>.\n\nThis is version: Alpha.",
        color=discord.Color.blue()
    )
    embed.set_footer(icon_url=bot.user.avatar.url, text=f"{bot.user}")

    await ctx.send(embed=embed)

bot.run(token)