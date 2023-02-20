'''Module to handle nickname functions'''
from src.wom import wom_lookup_user
import src.osp_logger as log

async def process_nickname_query(nickname_query):
    users = [u.strip() for u in nickname_query.split('|')]
    valid_users = [u for u in users if wom_lookup_user(u)]
    invalid_users = [u for u in users if u not in valid_users]
    return users, valid_users, invalid_users

async def update_member_nickname(member, nickname_query):
    log.info(f'Updating nickname for {member.nick} to {nickname_query}')
    await member.edit(nick=nickname_query)
