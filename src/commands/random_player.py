'''Example command module'''
from src.commands.base_command import BaseCommand
from src.utils                  import get_emoji
from random                 import randint
from src.settings import ALL_USERS
import json

class RandomVote(BaseCommand):
    TEAM_1_CHANNEL = 973034910996631562
    TEAM_2_CHANNEL = 973034965925265449

    '''Random command (example command)'''
    def __init__(self):
        description = "Pick a random person from bingo team"
        super().__init__(description, None, ALL_USERS)


    def roll(self, team):
        rolling = 0
        random_players = []
        while rolling != 3:
            rolled = randint(0, len(team) - 1)
            player = team[rolled]
            if player not in random_players:
                random_players.append(team[rolled])
                rolling += 1
        return random_players

    async def handle(self, params, message, client):
        team1 = []
        team2 = []
        actual_team = None
        with open('./team1.json', 'r') as f:
            team1 = json.load(f)

        with open('./team2.json', 'r') as f:
            team2 = json.load(f)
        
        if message.channel.id == self.TEAM_1_CHANNEL:
            actual_team = team1
        elif message.channel.id == self.TEAM_2_CHANNEL:
            actual_team = team2
        else:
            return await message.channel.send('Not in team chat channel!')
       
        print(message.channel.id)
        players = ', '.join(self.roll(actual_team))
        msg = f" You rolled {players}!"

        await message.channel.send(msg)
