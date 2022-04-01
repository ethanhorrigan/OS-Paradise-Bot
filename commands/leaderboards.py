'''Leaderboards command module'''
from commands.base_command import BaseCommand
from src.comp import Competition
from settings import ALL_USERS


class Leaderboards(BaseCommand):
    '''Leaderboards command'''

    def __init__(self):
        description = "Displays current BOTW/SOTW Leaderboards"
        super().__init__(description, None, ALL_USERS)

    async def handle(self, params, message, client):
        comp = Competition()
        display_amount = 10
        embed = comp.create_current_leaderboard_discord_embed(display_amount)
        await message.channel.send(embed=embed)
