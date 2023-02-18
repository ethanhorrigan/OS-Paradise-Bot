'''Common util functions'''
import discord.errors

async def send_embed(channel, embed):
    try:
        await channel.send(embed=embed)
    except discord.errors.DiscordException as e:
        print(f'Error sending embed: {e}')
