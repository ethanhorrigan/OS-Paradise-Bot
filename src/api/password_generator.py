import string
import random

def password_generator(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, \
        k=length))

print(password_generator(12))
