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

intents = discord.Intents.all()
# intents.messages = True
# intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)
#

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

# @client.command()
# async def ping(ctx):
#     await ctx.send('pong')


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


@client.command(help='testing help command')
async def last(ctx, team_number, year):
    team_number = int(team_number)
    year = int(year)
    # send a list of the last 5 events from team 4738
    events = tba.team_events(team_number, year)
    message = ''
    if len(events) == 0:
        await ctx.send(f'Team {team_number} did not compete in {year}')
    else:
        message += f'Team {team_number} competed in {year} at:\n'
        for event in events:
            message += f'{event.name}\n'
        await ctx.send(message)

@client.command()
async def awards(ctx, team_number, year):
    team_number = int(team_number)
    year = int(year)
    #send a list of the awards won by team_number in year
    awards = tba.team_awards(team_number, year)
    message = ""
    if len(awards) == 0:
        await ctx.send(f'Team {team_number} did not win any awards in {year}')
    else:
        message += (f'Team {team_number} won the following awards in {year}:\n')
        for award in awards:
            message += f"{award['name']}\n"
        await ctx.send(message)

#get a robot's stats using tba.team_robots(team_number)
@client.command()
async def robot(ctx, team_number):
    team_number = int(team_number)
    robot = tba.team_robots(team_number)
    print(robot)
    #loop through the list of robots and print out the name and year
    message = ""
    if len(robot) == 0:
        await ctx.send(f'Team {team_number} does not have any robots')
    else:
        message += (f'Team {team_number} has the following robots:\n')
        for robot in robot:
            message += f"{robot['robot_name']} in {robot['year']}\n"
        await ctx.send(message)

#get team's media using tba.team_media(team_number, year)
@client.command()
async def media(ctx, team_number, year):
    team_number = int(team_number)
    year = int(year)
    media = tba.team_media(team_number, year)
    print(media)
    message = ""
    if len(media) == 0:
        await ctx.send(f'Team {team_number} does not have any media from {year}')
    else:
        message += (f'Team {team_number} has the following media from {year}:\n')
        for media in media:
            #print media as an embed with the title as the media type and the description as the media direct link
            embed = discord.Embed(title=media['type'], description=media['direct_url'])
            await ctx.send(embed=embed)
            #
            # message += f"{media['type']} - {media['direct_url']}\n"
        await ctx.send(message)





client.run(TOKEN)
