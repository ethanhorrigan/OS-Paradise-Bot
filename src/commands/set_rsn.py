'''Discord Command: Setting Discord name with RSN'''
from src.commands.base_command import BaseCommand
from src.settings import ALL_USERS, SLEEP
from src.wom import wom_lookup_user

class SetRsn(BaseCommand):
    '''
    Discord Command for setting RSN
    Checks Wise old man to verify if RSN exists before setting discord name
    '''

    def __init__(self):
        description = 'Links RSN to Discord'
        params = ['rsn']
        super().__init__(description, params, ALL_USERS)

    async def handle(self, params, message, client):
        try:
            username_lookup = params[0]
            if len(username_lookup) > 12:
                return await message.channel.send(
                    'Username too long, cannot be greater than 12 characters',
                    delete_after=SLEEP)
            wom_res = wom_lookup_user(username_lookup)
            if 'message' in wom_res:
                return await message.channel.send(wom_res['message'],
                                                  delete_after=SLEEP)
        except (TypeError) as error:
            return await message.channel.send(error)

        await message.channel.send('Success')
