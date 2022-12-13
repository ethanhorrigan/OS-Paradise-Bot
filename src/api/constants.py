'''osp server constants'''
import os

RUN_SERVER = bool(os.getenv('RUN_FLASK_SERVER', 'True'))
