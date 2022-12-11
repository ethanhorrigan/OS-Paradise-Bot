"""Get all Users in Discord Command"""
from src.commands.base_command import BaseCommand
from src.settings import MOD, ALL_USERS, MOD_PERMISSIONS
import src.database.database as db
import src.osp_logger as log

class GetUsers(BaseCommand):
    """Get users class"""
    def __init__(self):
        description = 'Get all users and add to database for SOTW/BOTW'
        super().__init__(description, None, MOD)
        self.members = []

    def set_mentor_content(self, username):
        """Set content which mentor user will be added to database"""
        content_map = {
            'mr skeng man': {
                'content': 'COX,GWD',
                'consultant': False
            },
            'Hobo UwUber': {
                'content': 'COX,SOLO_COX,INFERNO,ZULRAH',
                'consultant': False
            },
            'Ruto': {
                'content': 'COX,SOLO_COX,GENERAL_PVM',
                'consultant': True
            },
            'x Dodgy x': {
                'content': 'TOB,INFERNO',
                'consultant': False
            },
            'ITIagicks': {
                'content': 'VORKATH,SEPULCHRE,GENERAL_PVM',
                'consultant': True
            },
            'Ethan': {
                'content': 'COX,TOB,GAUNTLET,GENERAL_PVM',
                'consultant': True
            }
        }
        return content_map.get(username)

    def set_permissions(self, role):
        return MOD if role in MOD_PERMISSIONS else ALL_USERS

    def handle_mulitple_users(self, display_name):
        accounts = display_name.split('|')
        for i, account in enumerate(accounts):
            if i == 0:
                log.info(f'{i} Main Account: {account.strip()}')
            else:
                log.info(f'{i} Alt Account: {account.strip()}')

    async def handle(self, params, message, client):
        """Handle command"""
        print(message.channel.name)
        for guild in client.guilds:
            print('guild', guild)
            if str(guild) != 'Horro':
                for member in guild.members:
                    display_name = str(member.display_name)
                    if '|' in display_name:
                        self.handle_mulitple_users(display_name)

                        self.members.append(member.display_name)
                    if '🤝Verified' in str(member.top_role) \
                        or '🤖 Bots' in str(member.top_role):
                        continue
                    else:
                        role = (str(member.top_role))
                        print(role)
                        permissions = self.set_permissions(role)

                        print(f'Name: {member.display_name} \nPermissions: \
                            {permissions}\nRole: {member.top_role}')
                        print(f'Roles: {member.roles}')
                        role_names = list(map(lambda n: n.name, member.roles))
                        role_names = ','.join(role_names)
                        consultant = False
                        content = None
                        if 'Mentor' in role_names:
                            content_dict = self.set_mentor_content(\
                                member.display_name)
                            print(f'Content: {content_dict}')
                            if content_dict is not None:
                                content = content_dict['content']
                                consultant = content_dict['consultant']
                        db.insert_members(str(member.id), \
                            str(member.display_name), str(member.top_role), \
                                permissions, role_names, content, consultant)
        # display_name, top_role, id, permissions, roles
        guilds = await client.fetch_guilds(limit=150).flatten()
        await message.channel.send('success')
