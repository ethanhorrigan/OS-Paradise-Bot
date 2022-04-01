"""Get all Users in Discord Command"""
from settings import ALL_USERS
from src.mentor_roles import MentorRoles
from commands.base_command import BaseCommand
import database.database as db
# Your friendly example event
# Keep in mind that the command name will be derived from the class name
# but in lowercase

# So, a command class named Random will generate a 'random' command
class GetMentor(BaseCommand):
    """Get users class"""
    all_content = [attr for attr in dir(MentorRoles) \
    if not callable(getattr(MentorRoles, attr)) and not attr.startswith("__")]
    str_content = ', '.join(all_content).title()

    def __init__(self):
        """Init command"""
        # A quick description for the help message
        description = "Mention mentor(s) for content you want to learn"
        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params'
        # argument in the handle() method
        # If no params are expected, leave this list empty or set it to None
        params = ["content name"]
        super().__init__(description, params, ALL_USERS)
    # Override the handle() method
    # It will be called every time the command is received
    def filter_mentors(self, all_mentors, user_content):
        """Return list of mentors for specified content"""
        mentor_roles = MentorRoles()
        mentor_names = []
        for mentors in all_mentors:
            name = mentors[0]
            content = str(mentors[1])
            if content != 'None':
                content = content.split(',')
                for content_type in content:
                    abr = mentor_roles.get_abbreviation(content_type)
                    if user_content in abr.lower() and name not in mentor_names:
                        mentor_names.append(f'<@{db.get_user_id_by_display_name(str(name))}>')
        return mentor_names

    async def handle(self, params, message, client):
        """Handle command"""

        content = "".join(params)
        content = content.lower()
        mentors = self.filter_mentors(db.get_mentors_for_content(), content)
        if len(mentors) != 0:
            msg = ', '.join(mentors)
        else:
            msg = 'Insufficient parameters! Please enter valid content.'
            msg += '\nCoX, CoX CM, ToB, Hardmode Tob, Vorkath, Zulrah, Solo cox, Gauntlet, \
                Inferno, Jad, Sepulchre, gwd, Nex, Nightmare'
            return await message.channel.send(message.author.mentions, msg)


        await message.channel.send(msg)
