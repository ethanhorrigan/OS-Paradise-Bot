'''Wise old man module'''
from src.database import database
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
        if 'message' in response:
            print(f'{user} not found')
            response = None
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
