import json
from src.wom import wom_lookup_user
import inflect

class ExperienceTracker():
    inflect_engine = inflect.engine()
    players_not_found = []
    starting_exp_slayer = 0
    starting_exp_farming = 0
    starting_exp_fishing = 0
    starting_exp_hunter = 0
    gained_exp_slayer = 0
    gained_exp_farming = 0
    gained_exp_fishing = 0
    gained_exp_hunter = 0
    current_exp_slayer = 0
    current_exp_farming = 0
    current_exp_fishing = 0
    current_exp_hunter = 0
    init = 0

    def __init__(self, team_name, init_boolean):
        self.init_boolean = init_boolean
        self.team_name = team_name
        self.team_data = self.open_json(f'{team_name}.json')
        if self.init_boolean is not True:
            self.team_exp_data = self.open_json(f'{team_name}_data.json')

    def open_json(self, file_name):
        '''Open json file and return team data'''
        with open(file_name, 'r') as f:
            data = json.load(f)
        return data

    def lookup_user(self, user_query):
        '''Retrieve all user details from wise old'''
        user = wom_lookup_user(user_query)
        if user is not None:
            slayer_exp = user['latestSnapshot']['slayer']['experience']
            farming_exp = user['latestSnapshot']['farming']['experience']
            hunter_exp = user['latestSnapshot']['hunter']['experience']
            fishing_exp = user['latestSnapshot']['fishing']['experience']
            self.gained_exp_slayer += slayer_exp
            self.gained_exp_farming += farming_exp
            self.gained_exp_hunter += hunter_exp
            self.gained_exp_fishing += fishing_exp
        else:
            print(f'{user_query}: not found')
            self.players_not_found.append(user_query)

    def team_exp_start_dict(self, team):
        '''Start team slayer exp'''
        return {
            'team': team,
            'slayer_exp_start': self.starting_exp_slayer,
            'slayer_exp_current': self.current_exp_slayer,
            'farming_exp_start': self.starting_exp_farming,
            'farming_exp_current': self.current_exp_farming,
            'fishing_exp_start': self.starting_exp_fishing,
            'fishing_exp_current': self.current_exp_fishing,
            'hunter_exp_start': self.starting_exp_hunter,
            'hunter_exp_current': self.current_exp_hunter,
            }

    def write_to_json(self, file_name, data):
        '''Write to json file'''
        with open(f'{file_name}.json', 'w') as f:
            json.dump(data, f, indent=2)

    def set_exp(self, _team_data):
        '''set starting exp'''
        self.starting_exp_slayer = _team_data['slayer_exp_start']
        self.starting_exp_farming = _team_data['farming_exp_start']
        self.starting_exp_fishing = _team_data['fishing_exp_start']
        self.starting_exp_hunter = _team_data['hunter_exp_start']

    def update_current_exp(self):
        self.current_exp_slayer = (self.starting_exp_slayer + self.gained_exp_slayer) - self.starting_exp_slayer
        print(f'Current slayer exp: {self.human_format(self.current_exp_slayer)}')
        print(f'gained slayer exp: {self.human_format(self.gained_exp_slayer)}')
        self.current_exp_farming = (self.starting_exp_farming + self.gained_exp_farming) - self.starting_exp_farming
        self.current_exp_fishing = (self.starting_exp_fishing + self.gained_exp_fishing) - self.starting_exp_fishing
        self.current_exp_hunter = (self.starting_exp_hunter + self.gained_exp_hunter) - self.starting_exp_hunter
    
    def init_exp(self):
        for player in tracker.team_data:
            tracker.lookup_user(player)
        self.starting_exp_slayer = self.gained_exp_slayer
        self.starting_exp_farming = self.gained_exp_farming
        self.starting_exp_fishing = self.gained_exp_fishing
        self.starting_exp_hunter = self.gained_exp_hunter
        exp_dict = tracker.team_exp_start_dict(self.team_name)
        print(exp_dict)
        exp_dict['init'] = 1
        return exp_dict

    def human_format(self, num):
        num = float('{:.3g}'.format(num))
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

tracker = ExperienceTracker('team1', True)

not_found = tracker.players_not_found
print(not_found)

if tracker.init_boolean:
    init = tracker.init_exp()

    tracker.write_to_json(f'{tracker.team_name}_data', init)

else:
    for player in tracker.team_data:
        tracker.lookup_user(player)
    tracker.set_exp(tracker.team_exp_data)
    tracker.update_current_exp()
    _exp_dict = tracker.team_exp_start_dict(tracker.team_name)
    tracker.write_to_json(f'{tracker.team_name}_data', _exp_dict)
    print(f'gained: {tracker.human_format(tracker.current_exp_slayer)}')