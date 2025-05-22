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

@bot.command() #Adds two numbers together
async def add(ctx, left: int, right: int):
    await ctx.send(left + right)

@bot.command() #Information embed command
async def info(ctx):
    embed = discord.Embed(
        description = "This is the info command for **Nerissa's Little Jailbird** bot, created by <@156500926880940032>.\n\nThis is version: Alpha.",
        color=discord.Color.blue()
    )
    embed.set_footer(icon_url=bot.user.avatar.url, text=f"{bot.user}")

    await ctx.send(embed=embed)

@bot.command() #lock command
async def lock(ctx):
    channel = ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)

    if overwrite.send_messages is False:
        await ctx.send(f"<#{channel.id}> is already locked.")
        return
    
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send(f"<#{channel.id}> has been locked.")


@bot.command() #unlock command
async def unlock(ctx):
    channel = ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)

    if overwrite.send_messages is True or None:
        await ctx.send(f"<#{channel.id}> is already unlocked.")
        return

    overwrite.send_messages = None
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send(f"<#{channel.id}> has been unlocked.")

# Run bot with token
bot.run(token)