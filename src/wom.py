'''Wise old man module'''
from src import settings
import requests


def wom_lookup_user(user):
    """Retrieve all user details from wise old man"""
    if len(user) < 12:
        response = 'Username too long, cannot be greater than 12 characters'
    url = f'https://api.wiseoldman.net/v2/players/{user}'
    try:
        request = requests.get(url)
        print(f'Lookup user response:{request.status_code}')
        if request.status_code == 404:
            response = f'{user} not found'
            return None
        response = request.json()
    except (requests.exceptions.RequestException, ValueError) as err:
        print(f'Error occurred: {err}')
        return None
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
