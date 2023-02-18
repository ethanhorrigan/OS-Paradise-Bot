import discord
from src.api.constants import number_words, pvm_content
# create a new client instance
client = discord.Client()

# create a function to generate the embed
async def generate_embed(title, content, channel):
    # create the embed object
    embed = discord.Embed(title=title, color=0xff0000)

    # add the content as a field
    embed.add_field(name='Content', value='\n'.join(content), inline=False)

    # add reactions based on the length of the content array

    reactions = [f':{number_words[i]}:' for i in range(1, len(content)-1)]

    message = await client.get_channel(channel).send(embed=embed)
    # add the reactions to the embed
    for reaction in reactions:
        embed.add_reaction(reaction)


# pvm_content_embed = generate_embed('PvM Content', pvm_content)
