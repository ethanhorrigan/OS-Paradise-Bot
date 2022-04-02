'''Help command module'''
from src.settings import ALL_USERS
from commands.base_command import BaseCommand

class Help(BaseCommand):

    def __init__(self):
        description = 'OS Paradise Help'
        super().__init__(description, None, ALL_USERS)

    async def handle(self, params, message, client):
        await message.channel.send('under development')
