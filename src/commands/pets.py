'''Pets command module'''
from src.settings import ALL_USERS
from commands.base_command import BaseCommand
import database.database as db
import discord
from random import randint


class Pet(BaseCommand):
    '''Handles pet command'''

    def __init__(self):
        description = "Get a random pet pic :)"
        super().__init__(description, None, ALL_USERS)

    async def handle(self, params, message, client):
        all_pets = db.get_pets()
        length_pets = len(all_pets)
        random_pet = all_pets[randint(0, length_pets)]
        embed = discord.Embed(color=discord.Color.orange())
        embed.set_image(url=random_pet[2])
        embed.set_footer(text=random_pet[1])

        await message.channel.send(embed=embed)
