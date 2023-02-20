"""A simple logger module for osp-bot"""
import discord
import datetime
from src import settings
from src.api import utils


def info(message: str):
    print(f'[{get_timestamp()}] INFO: {message}')

def warn(message: str):
    print(f'[{get_timestamp()}] WARN: {message}')

def error(message: str):
    print(f'[{get_timestamp()}] ERROR: {message}')

def get_timestamp():
    return datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')

async def send_rsn_update_message(client, new_member, member, nickname_query, \
    valid_users):

    rsn_log_channel = client.get_channel(settings.RSN_LOG_CHANNEL_ID)
    embed = discord.Embed(title='RSN Update', color=discord.Color.orange())
    if new_member:
        embed.add_field(name='New Member', value=nickname_query, inline=True)
    else:
        embed.add_field(name='Name', value=member.nick, inline=True)
        embed.add_field(name='Changed To', value=nickname_query, inline=True)
    print(f'Username(s) updated: {valid_users}')
    await utils.send_embed(rsn_log_channel, embed)
