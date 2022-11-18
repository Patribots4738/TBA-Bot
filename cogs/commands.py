# Importing the necessary modules for the client to work.
import os
from datetime import datetime
import tbapy
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('/.env/DISCORD_TOKEN')
TBA_TOKEN = os.getenv('/.env/TBA_TOKEN')

tba = tbapy.TBA(TBA_TOKEN)


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



class Commands(commands.Cog):

    def __init__(self, client):
        self.client = client
        print_message('success', 'client.cogs.commands', 'Loaded cogs.commands')

    # @commands.Cog.listener()
    # async def on_ready(self):
    #     print_message('success', 'client.cogs.commands', 'Loaded cogs.commands')

    @commands.command(help='testing help command')
    async def event(self, ctx, team_number, year):
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

            print_message('info', 'tba.team_events',
                               f'Successfully sent {team_number} events in year {year} to channel')

            await ctx.send(message)

    @commands.command()
    async def awards(self, ctx, team_number, year):
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

            print_message('info', 'tba.team_awards',
                               f'Successfully sent {team_number} awards in year {year} to channel')

            await ctx.send(message)

    @commands.command()
    async def media(self, ctx, team_number, year):
        team_number = int(team_number)
        year = int(year)
        # get team's media
        media = tba.team_media(team_number, year)
        # if there is no media
        if len(media) == 0:
            print_message('error', 'tba.team_media', f'No media found for team {team_number} in year {year}')
            await ctx.send(f'Team {team_number} has no media in {year}')
        # if there is media
        else:
            message = ""
            message += f'Team {team_number} has the following media in {year}:\n'
            # loop through media
            for media in media:
                # if media is a youtube video
                if media['type'] == 'youtube':
                    message += f"{media['type']} - {media['view_url']}\n"
                else:
                    message += f"{media['type']} - {media['direct_url']}\n"
            print_message('info', 'tba.team_media', f'Successfully sent {team_number} media in year {year} to channel')
            await ctx.send(message)

    @commands.command()
    async def alliance(self, ctx, event_key):
        # if the event key throws an error (not a valid event key) then send an error message to the channel
        try:
            alliances = tba.event_alliances(event_key)
            message = ""
            if len(alliances) == 0:
                print_message('error', 'tba.event_alliances', f'No alliances found for event 2022cabl')

                await ctx.send(f'No alliances found for event 2022cabl')

            else:
                # loop through alliances and get the teams, the first team is the captain and the rest are the picks
                # the captain is bolded
                # the picks are sent in an unordered list
                for alliance in alliances:
                    message += f"**{alliance['picks'][0]}**\n"
                    for pick in alliance['picks'][1:]:
                        # if the pick is the last pick in the list add an italicized tag around it
                        if pick == alliance['picks'][-1]:
                            message += f"*{pick}*\n"
                        else:
                            message += f"\t{pick}\n"
                    message += "\n"
                print_message('info', 'tba.event_alliances', f'Successfully sent alliance data to channel')

            await ctx.send(message)
        except:
            print_message('error', 'tba.event_alliances', f'No alliances found for event {event_key}')

            await ctx.send(f'No alliances found for event {event_key}')


async def setup(client):
    print(client)
    await client.add_cog(Commands(client))
