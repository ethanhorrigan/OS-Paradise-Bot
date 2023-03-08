'''Module to handle discord role functions'''

import discord
from src import settings


async def update_new_member_role(client, member):
    osp_client = client.get_guild(settings.OSP_GUILD_ID)

    sapphire_role_id = [role for role in osp_client.roles \
        if 'sapphire'.lower() in role.name.lower()]
    new_member_role_id = [role for role in osp_client.roles \
        if 'New to server'.lower() in role.name.lower()]
    emerald_role_id = [role for role in osp_client.roles \
        if 'emerald'.lower() in role.name.lower()]
    verified_role_id = [role for role in osp_client.roles \
        if 'verified'.lower() in role.name.lower()]

    sapphire_role = discord.utils.get(osp_client.roles,
                                      id=sapphire_role_id[0].id)
    new_member_role = discord.utils.get(osp_client.roles,
                                        id=new_member_role_id[0].id)
    emerald_role = discord.utils.get(osp_client.roles,
                                     id=emerald_role_id[0].id)
    verified_role = discord.utils.get(osp_client.roles,
                                      id=verified_role_id[0].id)


    new_member = new_member_role in member.roles
    if new_member:
        await member.add_roles(emerald_role[0].id, verified_role[0].id)
        await member.remove_roles(new_member_role[0].id)
    if sapphire_role in member.roles:
        await member.remove_roles(sapphire_role[0].id)
        await member.add_roles(emerald_role[0].id)
    return new_member
