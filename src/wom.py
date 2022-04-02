'''Wise old man module'''
import database.database as db
from src import settings, points
import requests

def wom_lookup_user(user):
    """Retrieve all user details from wise old man"""
    if len(user) < 12:
        response = 'Username too long, cannot be greater than 12 characters'
    url = f'https://api.wiseoldman.net/players/username/{user}'
    try:
        request = requests.get(url)
        response = request.json()
    except ValueError as err:
        print(err.__class__)
    return response


def get_original_name(display_name):
    og_name = ''
    try:
        r = requests.get(settings.wom_name_url(display_name)).json()
        if len(r) > 0:
            length = len(r) - 1
        else:
            length = len(r)
        og_name = r[length]['oldName']
    except requests.ConnectionError as err:
        print(err.__class__)

    return og_name


def get_all_display_names(display_name):
    r = requests.get(settings.wom_name_url(display_name)).json()
    a = []
    for i in range(len(r)):
        old_name = r[i]['oldName']
        new_name = r[i]['newName']
        a.append(f'{old_name} -> {new_name}')
    return '\n'.join(a[::-1])


def get_all_competitions():
    wom_group_url = 'https://api.wiseoldman.net/groups/'
    return requests.get(wom_group_url + settings.GROUP_ID \
        + '/competitions').json()


def get_all_ids():
    ids = []
    json = get_all_competitions()
    for i in json:
        ids.append(i['id'])
    return ids


def get_leaderboards_all_comps():
    ids = get_all_ids()
    db.create_table_rankings()
    for i in range(len(ids)):
        for j in range(3):
            print('get_leaderboards_all_comps Making request to WOM')
            result = requests.get(settings.WOM_URL + str(ids[i])).json()
            name = result['participants'][j]['displayName']
            # comp = (result['metric']).title()
            if db.check_if_user_exists_in_rankings(name):
                db.update_rankings(name, points.get_points(j))
            else:
                db.insert_rankings(str(name), points.get_points(j))
            print(f'{j} {name}')
