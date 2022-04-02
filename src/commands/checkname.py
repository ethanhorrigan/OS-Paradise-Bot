'''Checkname module'''

from src.commands.base_command import BaseCommand
from src.settings import ALL_USERS


class CheckName(BaseCommand):
    '''Handle Checkname functionality'''

    def __init__(self):
        description = 'Displays usernames for a given user'
        params = ['username']
        super().__init__(description, params, ALL_USERS)

    async def handle(self, params, message, client):
        pass
