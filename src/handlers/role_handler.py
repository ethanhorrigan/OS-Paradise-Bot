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
                                      name=sapphire_role_id[0].name)
    new_member_role = discord.utils.get(osp_client.roles,
                                        name=new_member_role_id[0].name)
    emerald_role = discord.utils.get(osp_client.roles,
                                     name=emerald_role_id[0].name)
    verified_role = discord.utils.get(osp_client.roles,
                                      name=verified_role_id[0].name)

    new_member = new_member_role in member.roles
    if new_member:
        await member.add_roles(emerald_role, verified_role)
        await member.remove_roles(new_member_role)
    if sapphire_role in member.roles:
        await member.remove_roles(sapphire_role)
        await member.add_roles(emerald_role)
    return new_member
