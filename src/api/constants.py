'''osp server constants'''
import os

RUN_SERVER = os.getenv('RUN_FLASK_SERVER', 'False')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DATABASE_URL = os.environ.get('DATABASE_URL')

pvm_content = [
    'God Wars Dungeon',
    'Chambers of Xeric',
    'Theatre of Blood',
    'Tombs of Amascut',
    'Dagannoth Kings',
    'Kalphite Queen',
    'Zulrah',
    'Vorkath',
    'Demonic Gorillas',
    'Thermonuclear Smoke Devil',
]

skilling_minigames = [
    'Tithe Farm',
    'Wintertodt',
    'Barbarian Assault',
    'Tempoross',
    'Guardians of the Rift',
    'Pyramid Plunder',
    'Hallowed Sepulchre',
    'Volcanic Mine',
]

number_words = {
    1: 'one',
    2: 'two',
    3: 'three',
    4: 'four',
    5: 'five',
    6: 'six',
    7: 'seven',
    8: 'eight',
    9: 'nine',
    10: 'keycap_ten'
}

number_emojis = [f':{number_words[i]}:' for i in range(1, 11)]
