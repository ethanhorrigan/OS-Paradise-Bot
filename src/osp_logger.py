import datetime

def info(message: str):
    print(f'[{datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}] INFO: {message}')

def warn(message: str):
    print(f'[{datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}] WARN: {message}')