'''Display commands module'''

from src.commands.base_command import BaseCommand
from src.settings import ALL_USERS, MOD, TEST_COMMAND


class Commands(BaseCommand):
    '''Command to display all available commands'''

    def __init__(self):
        description = "Displays this help message"
        params = None
        super().__init__(description, params, ALL_USERS)

    async def handle(self, params, message, client):
        from src.message_handler import COMMAND_HANDLERS
        msg = message.author.mention + "\n"

        # Displays all descriptions, sorted alphabetically by command name
        for cmd in sorted(COMMAND_HANDLERS.items()):
            if cmd[1].roleTag == TEST_COMMAND:
                continue
            if cmd[1].roleTag == MOD:
                continue
            if cmd[1].roleTag == ALL_USERS:
                msg += "\n" + cmd[1].description

        await message.channel.send(msg)
