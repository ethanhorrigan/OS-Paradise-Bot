"""Main module"""
import sys
import discord
from discord.ext import tasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src import message_handler, settings
from src.comp import Competition
import src.database.database as db

# Set to remember if the bot is already running, since on_ready may be called
# more than once on reconnects
this = sys.modules[__name__]
this.running = False

# Scheduler that will be used to manage events
sched = AsyncIOScheduler()


def main():
    """osp main"""
    # Initialize the client
    print('Starting up...')
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

            # pet_channel = client.get_channel(settings.PET_CHANNEL)
            # pet_channel_msgs = await pet_channel.history(limit=500).flatten()
            # for msg in pet_channel_msgs:
            #     if len(msg.attachments) > 0:
            #         for attachment in msg.attachments:
            #             if attachment.content_type != 'video/mp4':
            #                 db.insert_pets(attachment.id,
            #                                str(msg.author.display_name), str(
            #                                    attachment),
            #                                msg.created_at)

            channel = client.get_channel(684521702113280002)
            comp = Competition()
            if comp.running:
                embed = comp.create_current_leaderboard_discord_embed(10)
                await channel.send(embed=embed)
        display_current_comp_leaderboard_event.start()

    async def handle_new_pet_picture(message: discord.Message):
        if len(message.attachments) > 0:
            for attachment in message.attachments:
                if attachment.content_type != 'video/mp4':
                    db.insert_pets(attachment.id,
                        str(message.author.display_name), str(attachment),
                        message.created_at)
    # best to put it in here
    # The message handler for both new message and edits
    async def common_handle_message(message: discord.Message):
        if message.channel.id == settings.PET_CHANNEL:
            await handle_new_pet_picture(message)
        if message.type == discord.message.MessageType.new_member:
            handle_new_member(message)
        text = message.content
        if text.startswith(settings.COMMAND_PREFIX) \
                and text != settings.COMMAND_PREFIX:
            cmd_split = text[len(settings.COMMAND_PREFIX):].split()
            try:
                await message_handler.handle_command(
                    cmd_split[0].lower(), cmd_split[1:], message, client)
            except:
                print('Error while handling message', flush=True)
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
