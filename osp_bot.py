'''Main module'''
import sys
from time import sleep
import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src import message_handler, settings
import src.osp_logger as log
import src.database.database as db
import src.api.constants as server_constants
from src.events.leaderboards_event import \
    display_current_comp_leaderboard_event
from src.handlers.nickname_handler import update_member_nickname, \
    process_nickname_query
from src.handlers.role_handler import update_new_member_role

# Set to remember if the bot is already running, since on_ready may be called
# more than once on reconnects
this = sys.modules[__name__]
this.running = False

# Scheduler that will be used to manage events
sched = AsyncIOScheduler()


def main():
    '''osp main'''
    # Initialize the client
    log.info('Starting up...')
    intents = discord.Intents.all()
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

        display_current_comp_leaderboard_event.start(client)

    async def update_nickname(member: discord.message, nickname_query):
        log.info(f'Updating nickname for {member.nick}')
        try:
            users, valid_users, invalid_users = \
                await process_nickname_query(nickname_query)

            if len(valid_users) != len(users):
                print(f'Invalid username provided {invalid_users} \
                    Please try again.')
                return None

            if len(valid_users) == len(users):
                await update_member_nickname(member, nickname_query)

                db.update_member_nickname(member, nickname_query)

                new_member = await update_new_member_role(client, member)

                await log.send_rsn_update_message(client, new_member, member, \
                    nickname_query, valid_users)

        except Exception as e:
            log.info(e)

        return None

    async def handle_new_pet_picture(message: discord.Message):
        if len(message.attachments) > 0:
            for attachment in message.attachments:
                if attachment.content_type != 'video/mp4':
                    db.insert_pets(attachment.id,
                                   str(message.author.display_name), str(
                                       attachment),
                                   message.created_at)

    async def common_handle_message(message: discord.Message):
        if message.channel.id == settings.PET_CHANNEL:
            await handle_new_pet_picture(message)
        if message.channel.id in (settings.NEW_MEMBER_CHANNEL, \
            956498853283135531):
            channel = client.get_channel(684505358957281350)
            if message.content != 'Please enter a valid RSN.':
                if len(message.content) > 12 and '|' not in message.content:
                    await channel.send('Please enter a valid RSN.')
                else:
                    await update_nickname(message.author, message.content)
            try:
                sleep(2)
                await message.delete()
            except discord.NotFound:
                pass
        if message.type == discord.message.MessageType.new_member:
            handle_new_member(message)
        text = message.content

        if text.startswith(settings.COMMAND_PREFIX) \
                and text != settings.COMMAND_PREFIX:
            cmd_split = text[len(settings.COMMAND_PREFIX):].split()
            try:
                await message_handler.handle_command(
                    cmd_split[0].lower(), cmd_split[1:], message, client)
            except ValueError:
                print('Error while handling message', flush=True)
                raise

    def handle_new_member(message):
        '''Handles new member join'''
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

    @client.event
    async def on_raw_reaction_add(payload):
        guild = discord.utils.get(client.guilds, id=payload.guild_id)
        member = discord.utils.get(guild.members, id=payload.user_id)
        continents = {
            '🇺🇸': 'America',
            '🇪🇺': 'Europe',
            '🇦🇺': 'Australia',
        }
        emoji = payload.emoji.name
        if emoji in continents and member.nick is not None:
            role_to_assign = discord.utils.get(guild.roles, \
                name=continents[emoji])
            message = await client.get_channel(payload.channel_id)\
                .fetch_message(payload.message_id)
            await message.remove_reaction(emoji, member)
            print(f'{member.nick} reacted with {emoji}')

    client.run(settings.BOT_TOKEN)


if __name__ == '__main__':
    log.info(f'Starting OSP Server: {server_constants.RUN_SERVER}')
    if server_constants.RUN_SERVER == 'True':
        log.info('OSP Database connection established')

    if (settings.BOT_TOKEN is None) or (settings.BOT_TOKEN == ''):
        log.warn('Please set the BOT_TOKEN environment variable')

    if settings.BOT_TOKEN is not None:
        main()
