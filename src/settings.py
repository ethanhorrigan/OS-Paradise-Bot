"""Contains global settings and constants"""
from datetime import datetime
import os
import calendar
import numbers
import inflect

import src.database.database as db

inflectEngine = inflect.engine()

COMMAND_PREFIX = '!osp'
MOD = 'MOD'
ALL_USERS = 'ALL_USERS'
TEST_COMMAND = 'TEST_COMMAND'
DATABASE = 'resources/data.db'
GROUP_ID = '332'
CODE_BLOCK = '```'
# The bot token. Keep this secret!
BOT_TOKEN = os.environ.get('DISCORD_KEY', \
                            None)
# The now playing game. Set this to anything false-y ("", None) to disable it
NOW_PLAYING = COMMAND_PREFIX + ' commands'
# Base directory. Feel free to use it if you want.
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
WOM_URL = 'https://api.wiseoldman.net/v2/competitions/'
CURRENT_YEAR = datetime.now().year
CURRENT_MONTH = datetime.now().month
CURRENT_DAY = datetime.now().day
LAST_DAY_OF_THIS_MONTH = (calendar.monthrange(CURRENT_YEAR, CURRENT_MONTH))[-1]
MOD_PERMISSIONS = ['Paladin / Resort Manager', 'Max Relax (Leader)',
                   'Deputy Owner/Admiral']

OSP_GUILD_ID = 622716714387374100
PET_CHANNEL = 684833421834321920
NEW_MEMBER_CHANNEL = 684505358957281350
RSN_LOG_CHANNEL_ID = 685192535106125834
NEW_MEMBER_ROLE_ID = 684512685303529472
SAPPHIRE_ROLE_ID = 685925518394130500
EMERALD_ROLE_ID = 684515748789616664
VERIFIED_ROLE_ID = 684512685303529472

SLEEP = 15


def wom_name_url(current_username):
    """Retruns all OSRS usernames for given OSRS username"""
    return f'https://api.wiseoldman.net/v2/players/username/ \
        {current_username}/names'


def get_date_now():
    """Returns the current date"""
    date = datetime.now()
    return date.strftime('%d/%m/%y')


async def get_permissions(display_name):
    """Retrieve permissions avaiable to user"""
    permissions = await db.get_member_permissions(display_name)
    return permissions


def check_username_length(command):
    """Validates username length"""
    valid = False
    if isinstance(command, numbers.Integral):
        if command > 11:
            valid = False
        else:
            valid = True
    else:
        if len(command) > 0:
            valid = False
        else:
            valid = True
    return valid


def print_rankings(amount):
    """Prettifys rankings message"""
    msg = ''
    try:
        for i in range(amount):
            ordinal = inflectEngine.ordinal(i+1)
            msg += """ """
            msg += (f"""**{ordinal}**: {db.ranking_list[i].name} - \
                Score: { db.ranking_list[i].score}\n""")
    except TypeError as type_error:
        print(f'{type_error}. {amount} is not an integer.')
    return msg
