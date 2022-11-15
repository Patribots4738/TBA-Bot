# bot.py
import os
import tbapy

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TBA_TOKEN = os.getenv('TBA_TOKEN')

tba = tbapy.TBA(TBA_TOKEN)

intents = discord.Intents.default()
intents.messages = True
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.command()
async def clear(ctx, amount=5):
    """
    It deletes the command message and then deletes the amount of messages specified by the user

    :param ctx: The context of where the command was used
    :param amount: The amount of messages to delete, defaults to 5 (optional)
    """
    if amount == -00:
        await ctx.channel.purge()
    else:
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)


@client.command(name='last-robot', help='testing help command')
async def last(ctx):
    robot_year = tba.team_robots(4738)[-1].year
    robot_name = tba.team_robots(4738)[-1].robot_name
    await ctx.send(f"{robot_name} from team 4738 appeared in {robot_year}")


client.run(TOKEN)
