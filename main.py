import discord
from discord.ext import commands
from discord import app_commands
import os
import sys
import datetime
from dotenv import load_dotenv

load_dotenv() # Loads .env file

if os.path.exists(".env"):
    token = os.getenv('TOKEN') # Gets Token from .env file
    guild = discord.Object(os.getenv('GUILD_ID')) # Gets Guild ID for slash commands from .env file
else:
    if os.path.exists("error.log"):
        errorlog = open("error.log")
    else:
        errorlog = open("error.log", "x")
    
    with open("error.log", "a") as f:
        today = datetime.datetime.today()
        f.write(f"{today: %H:%M:%S %z - %B %d, %Y} - Error opening .env file.\n")
        sys.exit()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix='j?', intents=intents)

@client.event
async def on_ready():
    print(f"The bot is running as {client.user}")
    try:
        synced = await client.tree.sync(guild=guild)
        print(f"Synced {len(synced)} commands to guild {guild.id}")
    except Exception as e:
        print (f"Error syncing commands: {e}")

@client.event # Onboarding role trap
async def on_member_update(before, after):
    roletrap = 1374928771584495689
    roleupdate = set(after.roles) - set(before.roles)
    for role in roleupdate:
        if role.id == roletrap:
            try:
                await after.kick(reason="Onboarding role trap failed.")
                print(f"Kicked {after.name} for failing the Onboarding role trap.")
            except discord.Forbidden:
                print(f"Error kicking {after.name}: Missing permissions.")
            except Exception as e:
                print(f"Error kicking {after.name}:{e}.")

@client.tree.command(name="ping", description="Displays the bot latency", guild=guild)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f":ping_pong: **Pong!** Latency: {round(client.latency * 1000)}ms.")    

@client.tree.command(name="info", description="Displays the bot's info", guild=guild)
async def info(interaction: discord.Interaction):
    embed = discord.Embed(
        description = "This is the info command for **Nerissa's Little Jailbird** bot, created by <@156500926880940032>.\n\nThis is version: Alpha.",
        color=discord.Color.blue()
    )
    embed.set_footer(icon_url=client.user.avatar.url, text=f"{client.user}")
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="echo", description="Makes the bot send a message to a specific channel", guild=guild)
async def echo(interaction: discord.Interaction, channel: discord.TextChannel, message:str):
    try:
        await channel.send(message)
        await interaction.response.send_message(f"Sent!", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message(f"Couldn't send message: Missing permissions.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"Couldn't send message: {e}.", ephemeral=True)

@client.tree.command(name="lock", description="Command to lock a channel", guild=guild)
async def lock(interaction: discord.Interaction):
    overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
    if overwrite.send_messages is False:
        await interaction.response.send_message(f"<#{interaction.channel.id}> is already locked.")
        return
    overwrite.send_messages = False
    try:
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        await interaction.response.send_message(f"<#{interaction.channel.id}> has been locked.")
    except discord.Forbidden:
        await interaction.response.send_message(f"Failed to lock the channel: Missing permissions.")
    except Exception as e:
        await interaction.response.send_message(f"Failed to lock the channel: {e}")

@client.tree.command(name="unlock", description="Command to unlock a channel", guild=guild)
async def unlock(interaction: discord.Interaction):
    overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
    if overwrite.send_messages is True or overwrite.send_messages is None:
        await interaction.response.send_message(f"<#{interaction.channel.id}> is already unlocked.")
        return
    overwrite.send_messages = None
    try:
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        await interaction.response.send_message(f"<#{interaction.channel.id}> has been unlocked.")
    except discord.Forbidden:
        await interaction.response.send_message(f"Failed to unlock the channel: Missing permissions.")
    except Exception as e:
        await interaction.response.send_message(f"Failed to unlock the channel: {e}")

client.run(token)