# main.py
import os
import tbapy
from datetime import datetime
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Loading the .env file and getting the tokens from it.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TBA_TOKEN = os.getenv('TBA_TOKEN')

tba = tbapy.TBA(TBA_TOKEN)

# Setting the intents and prefixes for the bot.
intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)


@client.event
async def on_ready():
    """
    A function that is called when the bot is ready to start.
    """
    print_message('success', 'discord.client', 'Bot is connected to Discord')
    print_message('info', 'discord.client', 'Loading cogs.commands')
    await client.load_extension('cogs.commands')


@client.command()
async def clear(ctx, amount=1):
    """
    It clears the amount of messages you want to clear.

    :param ctx: The context of where the command was used
    :param amount: The amount of messages to delete, defaults to 1 (optional)
    """
    if amount == -00:
        await ctx.channel.purge()
    else:
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)


def print_message(type, subject, message):
    """
    It prints a message.

    :param type: The type of message to print. This can be one of the following:
    :param subject: The subject of the message
    :param message: The message to be printed
    """
    type = type.upper()

    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f'\033[30m{time}', end=' ')

    if type.lower() == 'success':
        print(f'\033[92m{type}', end=' ')

    elif type.lower() == 'warning':
        print(f'\033[93m{type}', end=' ')

    elif type.lower() == 'error':
        print(f'\033[91m{type}', end=' ')

    elif type.lower() == 'info':
        print(f'\033[94m{type}', end=' ')

    else:
        print(f'\033[30m{type}', end=' ')

    print(f'\033[95m{subject}', end=' ')

    print(f'\033[91m{message}')


client.run(TOKEN)
