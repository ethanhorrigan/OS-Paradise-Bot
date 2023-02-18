'''Leaderboards event'''
import src.api.utils as utils
from discord.ext import tasks

from src.comp import Competition

@tasks.loop(hours=1.0)
async def display_current_comp_leaderboard_event(client):
    '''Comp updater event'''
    channel = client.get_channel(684521702113280002)
    comp = Competition()
    if comp.running:
        embed = comp.create_current_leaderboard_discord_embed(10)
        await utils.send_embed(channel, embed)
