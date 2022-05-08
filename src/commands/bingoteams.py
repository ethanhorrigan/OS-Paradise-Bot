"""Get all Users in Discord Command"""
import discord
from src.settings import ALL_USERS
from src.mentor_roles import MentorRoles
from src.commands.base_command import BaseCommand
from src.bingo_names_parser import team1, team2

class BingoTeams(BaseCommand):
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
        embed = discord.Embed(title='Bingo Teams',
                              description='Teams for Bingo!',
                              color=discord.Color.orange())

        embed.add_field(name='Team 1', value='\n'.join(team1),
                        inline=True)
        embed.add_field(name='Team 2', value='\n'.join(team2),
                        inline=True)

        embed.set_footer(text=message.author.name,
                         icon_url=message.author.avatar_url)
        await message.channel.send(embed=embed)
