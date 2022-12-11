'''Prices module'''
from humanfriendly import format_timespan
import requests
import datetime as dt
import database.database as db

class Mapping:
    '''
    Mapping class
    Stores item_id, name, icon from OSRS item database
    '''
    def __init__(self, item_id, name, icon):
        self.item_id = item_id
        self.name = name
        self.icon = icon

class Prices:
    '''Retrieve prices data from OSRS Wiki'''
    OSRS_WIKI_ENPOINT = 'http://prices.runescape.wiki/api/v1/osrs/latest?'
    OSRS_MAPPING_ENPOINT = 'https://prices.runescape.wiki/api/v1/osrs/mapping'
    thresholds = {
        '100k': 100000,
        '1m': 1000000,
        '2.5m': 2500000,
        '5m': 5000000,
        '10m': 1000000,
        '100m': 10000000
    }

    def __init__(self):
        self.all_items = self.get_mapping_from_db() \
            if len(self.get_mapping_from_db()) > 0 else self.get_mapping()

    def get_mapping_from_db(self):
        mappings_list = []
        response = db.get_mappings()
        for item in response:
            mappings_list.append(Mapping(item[0], item[1], item[2]))
        return mappings_list

    def get_mapping(self):
        response = None
        mappings_list = []
        try:
            request = requests.get(self.OSRS_MAPPING_ENPOINT)
            response = request.json()
            for item in response:
                print(item['id'], item['name'])
                db.insert_mappings(
                    item['id'], item['name'], self.get_image_url(item['icon']))
                mappings_list.append(
                    Mapping(item['id'], item['name'], item['icon']))
        except requests.exceptions.RequestException as error:
            print(error)
        return mappings_list

    def get_icon(self, item_id):
        icon = None
        for item in self.all_items:
            if int(item.item_id) == int(item_id):
                icon = item.icon
        return icon

    def get_image_url(self, icon: str):
        formatted_icon = icon.replace(' ', '_')
        return 'https://oldschool.runescape.wiki/images' \
            f'/a/a2/{formatted_icon}?7263b'

    def format_time(self, time):
        pass

    @staticmethod
    def round_time(date_time: dt.timedelta):
        human_time = format_timespan(date_time.total_seconds())
        return human_time

    def get_threshold(self, threshold):
        pass

    def get_threshold_range(self, a: float, b: float):
        return range(a, b)

    def get_latest(self):
        response = None
        try:
            request = requests.get(self.OSRS_WIKI_ENPOINT)
            response = request.json()['data']
        except requests.exceptions.RequestException as err:
            print(err)
        return response

prices = Prices()
latest = prices.get_latest()
print(latest)

# create a function to print all keys in a dictionary
def print_dict(dictionary):
    for key in dictionary:
        print(key, dictionary[key])




