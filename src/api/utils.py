'''Common util functions'''
import discord
import discord.errors
import src.osp_logger as log

async def send_embed(channel, embed: discord.Embed):
    try:
        log.info(f'Sending embed: {embed.title} to {channel}')
        await channel.send(embed=embed)
    except discord.errors.DiscordException as e:
        log.error(f'Error sending embed: {e}')

async def get_role_from_guild(guild):
    return [role.name for role in guild.roles]
