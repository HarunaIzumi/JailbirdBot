from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
import logging
import json

load_dotenv() #Loads enviroment variables
token = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

client = commands.client(command_prefix="?", intents=intents)

@client.event
async def on_ready():
    print(f"The client is running as {client.user}")


@client.event # Onboarding client trap
async def on_member_update(before, after):
    
    role_trap = 1374928771584495689

    roles_before = set(before.roles)
    roles_after = set(after.roles)

    new_role = roles_after - roles_before

    for role in new_role:
        if role.id == role_trap:
            try:
                await after.kick(reason="Onboarding client trap failed.")
                print(f"Kicked {after.name} for failing the Onboarding client trap.")
            except discord.Forbidden:
                print(f"Missing permissions to kick {after.name}.")
            except Exception as e:
                print(f"Error kicking {after.name}:{e}.")


@client.command() #Information embed command
async def info(ctx):
    embed = discord.Embed(
        description = "This is the info command for **Nerissa's Little Jailbird** client, created by <@156500926880940032>.\n\nThis is version: Alpha.",
        color=discord.Color.blue()
    )
    embed.set_footer(icon_url=client.user.avatar.url, text=f"{client.user}")

    await ctx.send(embed=embed)

@client.command() #lock command
async def lock(ctx):
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)

    if overwrite.send_messages is False:
        await ctx.send(f"<#{ctx.channel.id}> is already locked.")
        return
    
    overwrite.send_messages = False
    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send(f"<#{ctx.channel.id}> has been locked.")


@client.command() #unlock command
async def unlock(ctx):
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)

    if overwrite.send_messages is True or None:
        await ctx.send(f"<#{ctx.channel.id}> is already unlocked.")
        return

    overwrite.send_messages = None
    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send(f"<#{ctx.channel.id}> has been unlocked.")

# Run client with token
client.run(token, log_handler=handler)