"""Get all Users in Discord Command"""
import discord
from src.settings import ALL_USERS
from src.mentor_roles import MentorRoles
from src.commands.base_command import BaseCommand
import src.database.database as db


class RegisterMentor(BaseCommand):
    """Register Mentor Command""" 
    # all_content = [attr for attr in dir(MentorRoles)
    #                if not callable(getattr(MentorRoles, attr)) and
    #                not attr.startswith('__')]
    # str_content = ', '.join(all_content).title()

    def __init__(self):
        """Init command"""
        description = 'Displays all mentors and content they teach!'
        super().__init__(description, None, ALL_USERS)

    async def handle(self, params, message, client):
        """Handle command"""

        continents = {
            "🇺🇸": "America",
            "🇪🇺": "Europe",
            "🇦🇺": "Australia",
        }

        timezone_embed = discord.Embed(title="Select Your Timezone")
        for emoji, continent in continents.items():
            timezone_embed.add_field(name=emoji, value=continent, inline=True)

        msg = await message.channel.send(embed=timezone_embed)
        for emoji in continents.keys():
            await msg.add_reaction(emoji)


        # await message.channel.send(embed=embed)
