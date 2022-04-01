from commands.base_command import BaseCommand
from settings import ALL_USERS, TEST_COMMAND, MOD

# This is a convenient command that automatically generates a helpful
# message showing all available commands
class Commands(BaseCommand):
    def __init__(self):
        description = "Displays this help message"
        params = None
        super().__init__(description, params, ALL_USERS)

    async def handle(self, params, message, client):
        from message_handler import COMMAND_HANDLERS
        msg = message.author.mention + "\n"

        # Displays all descriptions, sorted alphabetically by command name
        for cmd in sorted(COMMAND_HANDLERS.items()):
            if (cmd[1].roleTag == TEST_COMMAND):
                continue
            if (cmd[1].roleTag == MOD):
                continue
            if (cmd[1].roleTag == ALL_USERS):
                msg += "\n" + cmd[1].description

        await message.channel.send(msg)
