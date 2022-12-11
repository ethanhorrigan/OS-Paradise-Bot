"""Competitions from wiseoldman"""
import datetime
import inflect
import requests
import discord
from time import sleep
import src.osp_logger as log


class TooManyClientsError(Exception):
    log.warn('Too many clients already connected to the server')
    pass

class LeaderboardEntry:
    """Object for leaderboard entries
    New instance for this class is called on each command/event
    Parameters
    -----------
    position: :class:`str`
        The position in leaderboards as ordinal.
    name: :class:`str`
        The OSRS username.
    gained: :class:`int`
        The experience or killcount gained during the competition.
    """

    def __init__(self, position, name, gained):
        self.position = position
        self.name = name
        self.gained = gained

    def __str__(self):
        return f'{self.position}: {self.name} ({self.gained})'


class Competition:
    """Handles functionality for wiseoldman competitions"""

    inflect_engine = inflect.engine()
    GROUP_ID = '332'
    WOM_URL = 'https://api.wiseoldman.net/competitions/'
    WOM_GROUP_URL = 'https://api.wiseoldman.net/groups/'
    IMAGE_URL = 'https://oldschool.runescape.wiki/images/'

    def __init__(self):
        self.competitions = self.get_competitions()
        self._current_comp_id = self.current_comp_id()
        log.info(f'Current competition ID: {self._current_comp_id}')
        self._current_comp_name = self.current_comp_name()
        log.info(self._current_comp_name)
        self.metric = self.current_comp_metric()
        log.info(self.metric)
        self.image = self.validate_image_url(
            f'{self.IMAGE_URL}{self.metric.title()}.png')
        self.running = self.is_competition_running()
        log.info(f'Competition running: {self.running}')

    def get_competitions(self, retries=3, timeout=15):
        """Return a list of competitions from wise old man"""
        for i in range(retries):
            log.info(f'get_competitions attempt {i + 1} of {retries}')
            try:
                url = self.WOM_GROUP_URL + self.GROUP_ID + '/competitions'
                log.info(f'Executing request to: {url}')
                competitions = requests.get(url).json()
                if 'message' in competitions and competitions['message']\
                     == 'sorry, too many clients already':
                    raise TooManyClientsError(
                        'Too many clients are already connected to the server')
                else:
                    return competitions
            except requests.exceptions.RequestException as exception:
                log.info(exception)
            except TooManyClientsError as exception:
                log.warn(exception)
            log.info(f'Waiting {timeout} seconds before retrying')
            sleep(timeout)

        return None

    def current_comp_id(self):
        """Return the current competition id"""
        log.info('Getting current competition id')
        return str(self.competitions[0]['id'])

    def current_comp_name(self):
        """Return the current competition name"""
        log.info('Getting current competition name')
        return str(self.competitions[0]['title'])

    def current_comp_metric(self):
        """Return the current competition name"""
        log.info('Getting current competition metric')
        return str(self.competitions[0]['metric'])

    def validate_image_url(self, image_url):
        """Validates an image url returns correctly
        else returns default image
        """
        final_url = image_url
        try:
            request = requests.get(image_url)
            if request.status_code == 402:
                final_url = 'https://oldschool.runescape.wiki' \
                    + '/images/thumb/Boss.png/1244px-Boss.png'
        except requests.exceptions.RequestException as exception:
            log.info(exception)
        return final_url

    def get_leaderboards_current_comp(self, display_amount):
        """Returns gained exp/kc for current comp"""
        results = []
        wom_gained_url = f'{self.WOM_URL}{self._current_comp_id}'
        try:
            request = requests.get(wom_gained_url)
            response = request.json()
            for i in range(display_amount):
                name = response['participants'][i]['displayName']
                gained = response['participants'][i]['progress']['gained']
                ordinal_pos = self.get_oridinal(i+1)
                results.append(LeaderboardEntry(ordinal_pos, name, gained))
        except requests.exceptions.RequestException as err:
            log.info(err)
        return results

    def create_current_leaderboard_discord_embed(self, display_amount):
        """Returns discord embed for current leaderboard"""
        embed = discord.Embed(title=f'{self._current_comp_name} Leaderboards',
                              color=discord.Color.orange())
        positions = [str(x.position) for x in
                     self.get_leaderboards_current_comp(display_amount)]
        names = [x.name for x in
                 self.get_leaderboards_current_comp(display_amount)]
        gained = [str(x.gained) for x in
                  self.get_leaderboards_current_comp(display_amount)]
        metric = self.get_comp_metric_type(self._current_comp_name)
        comp_title = self._current_comp_name.title().replace('_', ' ')
        embed.add_field(name='Position', value='\n'.join(positions),
                        inline=True)
        embed.add_field(name='Name', value='\n'.join(names), inline=True)
        embed.add_field(name=metric, value='\n'.join(gained), inline=True)
        embed.set_footer(text=comp_title, icon_url=self.image)
        return embed

    def get_oridinal(self, number):
        """Returns the ordinal for give number"""
        try:
            oridnal = self.inflect_engine.ordinal(number)
        except TypeError as type_error:
            log.info(f'{type_error}: Only integers are allowed')
        return oridnal

    @staticmethod
    def get_comp_metric_type(comp):
        """Return competition metric type"""
        type_abr = 'SOTW' if 'SOTW' in comp else 'BOTW'
        metric_type = 'XP Gained'
        if type_abr == 'BOTW':
            metric_type = 'Killed'
        return metric_type

    @staticmethod
    def format_date_time(date_time):
        """Formats date timedelta into a string"""
        year = date_time[:4]
        month = date_time[5:7]
        day = date_time[8:10]
        hour = date_time[11:13]
        minute = date_time[14:16]
        return datetime.datetime(int(year), int(month),
                                 int(day), int(hour), int(minute))

    @staticmethod
    def get_ordinal_day(day):
        """Return days as string"""
        return 'day' if day == 1 else 'days'

    def get_comp_start_date(self):
        """Return the current competition start date"""
        return str(self.competitions[0]['startsAt'])

    def get_comp_end_date(self):
        """Return the current competition end date"""
        try:
            url = self.WOM_GROUP_URL + self.GROUP_ID + '/competitions'
            res = str(self.competitions[0]['endsAt'])
            date_formatted = self.format_date_time(res)
            datetime_until = date_formatted - datetime.datetime.now()
            now = datetime.datetime.now()
            now = datetime.datetime(
                now.year, now.month, now.day, now.hour, now.minute)
        except requests.exceptions.RequestException as err:
            log.warn(err)
        return [now, date_formatted]

    def is_competition_running(self):
        running = False
        current_comp = self.get_comp_end_date()
        if current_comp[0].date() < current_comp[1].date():
            running = True
        elif current_comp[0].date() == current_comp[1].date():
            if current_comp[0].time() < current_comp[1].time():
                running = True
        return running

    def get_comp_end_time(self):
        """Return the current competition end time"""
        try:
            res = str(self.competitions[0]['endsAt'])
            date_formatted = self.format_date_time(res)
            datetime_until = date_formatted - datetime.datetime.now()
            now = datetime.datetime.now()
            now = datetime.datetime(
                now.year, now.month, now.day, now.hour, now.minute)
        except requests.exceptions.RequestException as err:
            log.info(err)
        return datetime_until

    def get_comp_start_time(self):
        """Return the current competition start time"""
        try:
            url = self.WOM_GROUP_URL + self.GROUP_ID + '/competitions'
            res = str(self.competitions[0]['startsAt'])
            date_formatted = self.format_date_time(res)
        except requests.exceptions.RequestException as err:
            log.info(err)
        return date_formatted

