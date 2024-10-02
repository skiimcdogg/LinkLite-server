import string, random

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits

    while True:
        short_code = ''.join(random.sample(characters, length))

        if any(char.isdigit() for char in short_code):
            return short_code