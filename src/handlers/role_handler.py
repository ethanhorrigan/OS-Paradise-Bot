'''Module to handle discord role functions'''

import discord
from src import settings


async def update_new_member_role(client, member):
    osp_client = client.get_guild(settings.OSP_GUILD_ID)
    sapphire_role = discord.utils.get(osp_client.roles,
                                      id=settings.SAPPHIRE_ROLE_ID)
    new_member_role = discord.utils.get(osp_client.roles,
                                        id=settings.NEW_MEMBER_ROLE_ID)
    emerald_role = discord.utils.get(osp_client.roles,
                                     id=settings.EMERALD_ROLE_ID)
    verified_role = discord.utils.get(osp_client.roles,
                                      id=settings.VERIFIED_ROLE_ID)

    new_member = new_member_role in member.roles
    if new_member:
        await member.add_roles(emerald_role, verified_role)
        await member.remove_roles(new_member_role)
    if sapphire_role in member.roles:
        await member.remove_roles(sapphire_role)
        await member.add_roles(emerald_role)
    return new_member
