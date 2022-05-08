'''Bingo Names Parser'''
import requests
from operator import itemgetter
import json

WISE_OLD_MAN_BASE_URL = 'https://api.wiseoldman.net'

with open('src/bingo_names.txt') as f:
    lines = f.readlines()

leftToAdd = []
players = []

def wom_lookup_user(user):
    """Retrieve all user details from wise old man"""
    if len(user) < 12:
        response = 'Username too long, cannot be greater than 12 characters'
    url = f'{WISE_OLD_MAN_BASE_URL}/players/username/{user}'
    try:
        request = requests.get(url)
        response = request.json()
        if 'message' in response:
            print(f'{user} not found')
            leftToAdd.append(user)
        else:
            username = response['username']
            ehb = response['ehb']
            # ehb = round(ehb)
            ehp = response['ehp']
            country = response['country']
            build_type = response['type']
            average = ehb + ehp / 2
            average = round(average)
            # print(f'{username} average: {average} country: {country} type: {_type}')
            # player_dict = {'username': username, 'average': average}
            print(f'{username} ehb: {ehb} country: {country} type: {build_type}')
            player_dict = {'username': username, 'ehb': ehb, 'ehp': ehp}
            players.append(player_dict)

    except ValueError as err:
        print(err.__class__)
    return response


for line in lines:
    _username = line.strip()
    wom_lookup_user(_username)

newlist = sorted(players, key=itemgetter('ehp', 'ehb'), reverse=True)

for p in newlist:
    print(f'{p["username"]} ehb: {p["ehb"]} ehp: {p["ehp"]}')
# add left to add to list
for l in leftToAdd:
    newlist.append({'username': l, 'average': 0})

# put every other element into seperate lists
even = []
odd = []
for i, player in enumerate(newlist):
    if i % 2 == 0:
        even.append(player)
    else:
        odd.append(player)

print(len(even))
print(len(odd))

team1 = []
team2 = []
for player in even:
    team1.append(player['username'])
for player in odd:
    team2.append(player['username'])

with open('team1.json', 'w') as f:
    json.dump(team1, f, ensure_ascii=False, indent=4)

with open('team2.json', 'w') as f:
    json.dump(team2, f, ensure_ascii=False, indent=4)
