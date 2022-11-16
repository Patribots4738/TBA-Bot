# bot.py
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


@client.command(help='testing help command')
async def last(ctx, team_number, year):
    team_number = int(team_number)
    year = int(year)

    events = tba.team_events(team_number, year)

    message = ''
    if len(events) == 0:
        print_message('error', 'tba.team_events', f'No events found for team {team_number} in year {year}')

        await ctx.send(f'Team {team_number} did not compete in {year}')

    else:
        message += f'Team {team_number} competed in {year} at:\n'

        for event in events:
            message += f'{event.name}\n'

        print_message('info', 'tba.team_events', f'Successfully sent {team_number} events in year {year} to channel')

        await ctx.send(message)


@client.command()
async def awards(ctx, team_number, year):
    team_number = int(team_number)
    year = int(year)

    awards = tba.team_awards(team_number, year)

    message = ""
    if len(awards) == 0:
        print_message('error', 'tba.team_awards', f'No awards found for team {team_number} in year {year}')

        await ctx.send(f'Team {team_number} did not win any awards in {year}')

    else:
        message += (f'Team {team_number} won the following awards in {year}:\n')

        for award in awards:
            message += f"{award['name']}\n"

        print_message('info', 'tba.team_awards', f'Successfully sent {team_number} awards in year {year} to channel')

        await ctx.send(message)


# get a robot's stats using tba.team_robots(team_number)
@client.command()
async def robot(ctx, team_number):
    team_number = int(team_number)
    robot = tba.team_robots(team_number)

    message = ""
    if len(robot) == 0:
        print_message('error', 'tba.team_robots', f'No robots found for team {team_number}')

        await ctx.send(f'Team {team_number} does not have any robots')

    else:
        message += (f'Team {team_number} has the following robots:\n')

        for robot in robot:
            message += f"{robot['robot_name']} in {robot['year']}\n"

        print_message('info', 'tba.team_robots', f'Successfully sent {team_number} robots to channel')

        await ctx.send(message)


# get team's media using tba.team_media(team_number, year)
@client.command()
async def media(ctx, team_number, year):
    team_number = int(team_number)
    year = int(year)

    medias = tba.team_media(team_number, year)

    message = ""
    if len(medias) == 0:
        print_message('error', 'tba.team_media', f'No media found for team {team_number} in year {year}')

        await ctx.send(f'Team {team_number} does not have any media from {year}')

    else:
        message += f'Team {team_number} has the following media from {year}:\n'

        for media in medias:
            embed = discord.Embed(title=media['type'], description=media['direct_url'])

            await ctx.send(embed=embed)

        print_message('info', 'tba.team_media', f'Successfully sent {team_number} media from {year} to channel')

        await ctx.send(message)


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
