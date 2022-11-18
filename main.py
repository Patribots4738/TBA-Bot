# main.py
import os
import tbapy
from datetime import datetime
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TBA_TOKEN = os.getenv('TBA_TOKEN')

tba = tbapy.TBA(TBA_TOKEN)

intents = discord.Intents.all()

client = commands.Bot(command_prefix='!', intents=intents)


@client.event
async def on_ready():
    print_message('success', 'discord.client', 'Bot is connected to Discord')
    print_message('info', 'discord.client', 'Loading cogs.commands')
    await client.load_extension('cogs.commands')


'''
It deletes the command message and then deletes the amount of messages specified by the user

@param ctx: The context of where the command was used
@param amount: The amount of messages to delete, defaults to 5 (optional)
'''


@client.command()
async def clear(ctx, amount=1):
    if amount == -00:
        await ctx.channel.purge()
    else:
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)

'''
method to print the time of the message in black and any message to the console in color given the type of message, subject the message itself
@param type: the type of message to print
@param message: the message to print
@param subject: the subject of the message
the subject is always printed in pink
the message is always printed in light red
the type is printed in the color corresponding to the type

ex: 2022-11-15 15:52:09 INFO     discord.client logging in using static token
'''


def print_message(type, subject, message):
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
