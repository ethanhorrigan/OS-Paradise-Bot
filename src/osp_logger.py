"""A simple logger module for osp-bot"""
import datetime


def info(message: str):
    print(f'[{get_timestamp()}] INFO: {message}')


def warn(message: str):
    print(f'[{get_timestamp()}] WARN: {message}')


def get_timestamp():
    return datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
