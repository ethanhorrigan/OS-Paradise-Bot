'''Example command module'''
from src.commands.base_command import BaseCommand
from src.utils                  import get_emoji
from random                 import randint
from src.settings               import TEST_COMMAND

class Random(BaseCommand):
    '''Random command (example command)'''
    def __init__(self):
        description = "Generates a random number between two given numbers"
        params = ["lower", "upper"]
        super().__init__(description, params, TEST_COMMAND)

    async def handle(self, params, message, client):

        try:
            lower_bound = int(params[0])
            upper_bound = int(params[1])
        except ValueError:
            await message.channel.send("Please, provide valid numbers")
            return

        if lower_bound > upper_bound:
            await message.channel.send("The lower bound can't be higher than \
                the upper bound")
            return

        rolled = randint(lower_bound, upper_bound)
        msg = get_emoji(":game_die:") + f" You rolled {rolled}!"

        await message.channel.send(msg)
