'''Message handler module'''
from src.commands import *
from src import settings
from src.commands import base_command

COMMAND_HANDLERS = {c.__name__.lower(): c()
                    for c in base_command.BaseCommand.__subclasses__()}

print(COMMAND_HANDLERS)
async def handle_command(command, args, message, bot_client):
    if command not in COMMAND_HANDLERS:
        return

    print(f"{message.author.name}: {settings.COMMAND_PREFIX}{command} "
          + " ".join(args))

    cmd_obj = COMMAND_HANDLERS[command]
    if cmd_obj.params and len(args) < len(cmd_obj.params):
        await message.channel.send(message.author.mention + " \
            Insufficient parameters!")
    else:
        print('cmd_obj.handle(args, message, bot_client)')
        await cmd_obj.handle(args, message, bot_client)

