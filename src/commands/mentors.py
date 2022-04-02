"""Get all Users in Discord Command"""
import discord
from src.settings import ALL_USERS
from src.mentor_roles import MentorRoles
from src.commands.base_command import BaseCommand
import src.database.database as db


class Mentors(BaseCommand):
    """Get users class"""
    all_content = [attr for attr in dir(MentorRoles)
                   if not callable(getattr(MentorRoles, attr)) and
                   not attr.startswith('__')]
    str_content = ', '.join(all_content).title()

    def __init__(self):
        """Init command"""
        description = 'Displays all mentors and content they teach!'
        super().__init__(description, None, ALL_USERS)

    async def handle(self, params, message, client):
        """Handle command"""
        all_mentors = db.get_mentors_for_content()
        embed = discord.Embed(title='Mentors',
                              description='All Mentors in OS Paradise!',
                              color=discord.Color.orange())
        names_list = []
        content_list = []
        for mentor in all_mentors:
            name = mentor[0]
            content = mentor[1]
            abbreviations = []
            if name is not None and content is not None:
                names_list.append(name)
                content = content.split(',')
                mentor_roles = MentorRoles()
                for c_name in content:
                    abr = mentor_roles.get_abbreviation(c_name)
                    print(f'content: {c_name} abr: {abr}')
                    abbreviations.append(abr)
                abbreviations = ', '.join(abbreviations)
                content_list.append(abbreviations)

        embed.add_field(name='Mentor', value='\n'.join(names_list),
                        inline=True)
        embed.add_field(name='Content', value='\n'.join(content_list),
                        inline=True)

        embed.set_footer(text=message.author.name,
                         icon_url=message.author.avatar_url)
        await message.channel.send(embed=embed)
