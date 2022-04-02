'''Base command module'''
from src import settings


class BaseCommand:
    '''Handles command functionality'''

    def __init__(self, description, params, role_tag):
        self.name = type(self).__name__.lower()
        self.params = params
        self.role_tag = role_tag

        desc = f"**{settings.COMMAND_PREFIX} {self.name}**"

        if self.params:
            desc += " " + " ".join(f"*<{p}>*" for p in params)

        desc += f": {description}."
        self.description = desc

    async def handle(self, params, message, client):
        raise NotImplementedError  # To be defined by every command
