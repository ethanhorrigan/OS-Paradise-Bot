'''Current BOTW/SOTW module'''

from src.commands.base_command import BaseCommand
from src import wom
from src.settings import ALL_USERS


class Current(BaseCommand):
    '''Handle functionality for current Botw/Sotw command'''

    def __init__(self):
        description = 'Displays current BOTW/SOTW Competiton'
        super().__init__(description, None, ALL_USERS)

    async def handle(self, params, message, client):
        msg = f'{wom.get_current_comp()}\n{wom.get_leaderboards()}'
        await message.channel.send(msg)
