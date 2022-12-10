"""Main module"""
import sys
from time import sleep
import discord
from discord.ext import tasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src import message_handler, settings
import src.osp_logger as log
from src.comp import Competition
import src.database.database as db
from src.wom import wom_lookup_user

# Set to remember if the bot is already running, since on_ready may be called
# more than once on reconnects
this = sys.modules[__name__]
this.running = False

# Scheduler that will be used to manage events
sched = AsyncIOScheduler()


def main():
    """osp main"""
    # Initialize the client
    log.info('Starting up...')
    intents = discord.Intents.default()
    intents.members = True
    intents.presences = True
    intents.guilds = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        if this.running:
            return

        this.running = True

        # Set the playing status
        if settings.NOW_PLAYING:
            print('Setting NP game', flush=True)
            await client.change_presence(
                activity=discord.Game(name=settings.NOW_PLAYING))
        print('Logged in!', flush=True)

        @tasks.loop(hours=1.0)
        async def display_current_comp_leaderboard_event():
            """Comp updater event"""
            channel = client.get_channel(684521702113280002)
            comp = Competition()
            if comp.running:
                embed = comp.create_current_leaderboard_discord_embed(10)
                await channel.send(embed=embed)
        display_current_comp_leaderboard_event.start()




    async def update_nickname(member: discord.message, nickname_query):
        nickname_valid = False
        new_member = False
        nickname = member.nick

        rsn_log_channel = client.get_channel(685192535106125834)

        embed = discord.Embed(title='RSN Update', color=discord.Color.orange())
        role_ids = []
        for role in member.roles:
            role_ids.append(role.id)

        if '|' in nickname_query:
            users = nickname_query.split('| ')
            main_account = users[0].strip()
            alt_account = users[1].strip()
            log.info(main_account, alt_account)
            for u in users:
                log.info(f'searching for username: {u}')
                if wom_lookup_user(u) is not None:
                    log.info(f'{nickname_query} user valid.')
                    nickname_valid = True
                else:
                    nickname_valid = False
                    return None
        else:
            if wom_lookup_user(nickname_query) is not None:
                log.info(f'{nickname_query} user valid.')
                nickname_valid = True
        osp_client = client.get_guild(622716714387374100)
        log.info(osp_client)
        sapphire_role = osp_client.get_role(settings.SAPPHIRE_ROLE_ID)
        new_member_role = osp_client.get_role(settings.NEW_MEMBER_ROLE_ID)
        emerald_role = osp_client.get_role(settings.EMERALD_ROLE_ID)
        verified_role = osp_client.get_role(settings.VERIFIED_ROLE_ID)


        if settings.NEW_MEMBER_ROLE_ID in role_ids:
            new_member = True
            await member.add_roles(emerald_role)
            await member.add_roles(verified_role)
            await member.remove_roles(new_member_role)
        if settings.SAPPHIRE_ROLE_ID in role_ids:
            await member.remove_roles(sapphire_role)
            await member.add_roles(emerald_role)

        if nickname_valid:
            await member.edit(nick=nickname_query)
            if new_member:
                embed.add_field(name='New Member',
                                value=nickname_query, inline=True)
            else:
                embed.add_field(name='Name', value=nickname, inline=True)
                embed.add_field(name='Changed To', value=nickname_query,
                inline=True)
            await rsn_log_channel.send(embed=embed)
        return None

    async def handle_new_pet_picture(message: discord.Message):
        if len(message.attachments) > 0:
            for attachment in message.attachments:
                if attachment.content_type != 'video/mp4':
                    db.insert_pets(attachment.id,
                                   str(message.author.display_name), str(
                                       attachment),
                                   message.created_at)
    # best to put it in here
    # The message handler for both new message and edits

    async def common_handle_message(message: discord.Message):
        log.info(f'message {message}')
        log.info(f'message.content {message.content}')
        if message.channel.id == settings.PET_CHANNEL:
            await handle_new_pet_picture(message)
        if message.channel.id == settings.NEW_MEMBER_CHANNEL:
            channel = client.get_channel(684505358957281350)
            if message.content != 'Please enter a valid RSN.':
                if len(message.content) > 12 and '|' not in message.content:
                    await channel.send('Please enter a valid RSN.')
                    sleep(3)
                    await message.delete()
                else:
                    await update_nickname(message.author, message.content)
                    await message.delete()
            sleep(5)
            await message.delete()
        if message.type == discord.message.MessageType.new_member:
            handle_new_member(message)
        text = message.content
        log.info(f'handling message {text}')
        log.info(f'command prefix: {settings.COMMAND_PREFIX}')
        if text.startswith(settings.COMMAND_PREFIX) \
                and text != settings.COMMAND_PREFIX:
            cmd_split = text[len(settings.COMMAND_PREFIX):].split()
            print(f'cmd_split: {cmd_split}')
            try:
                await message_handler.handle_command(
                    cmd_split[0].lower(), cmd_split[1:], message, client)
            except:
                log.info('Error while handling message', flush=True)
                raise

    def handle_new_member(message):
        """Handles new member join"""
        db.insert_members(message.author.name, 'New', message.author.id,
                          settings.ALL_USERS, 'New', None, False)

    @client.event
    async def on_member_update(before, after):
        before_nickname = str(before.nick)
        after_nickname = str(after.nick)
        before_roles = str(before.roles)
        after_roles = str(after.roles)

        if after_nickname is not None:
            if before_nickname != after_nickname:
                db.update_member_nickname(before.id, after_nickname)
        if before_roles != after_roles:
            db.update_member_roles(before_nickname, after_roles)

    @client.event
    async def on_message(message):
        await common_handle_message(message)

    @client.event
    async def on_message_edit(after):
        await common_handle_message(after)

    client.run(settings.BOT_TOKEN)


if __name__ == '__main__':
    main()
