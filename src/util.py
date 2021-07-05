import string
import random
from time import sleep
from typing import List
import requests
from socketio import Client as SocketClient

base_url = "http://localhost"


def generate_word(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def generate_email():
    return f"{generate_word(8)}@energify.pt"


def request(endpoint: str, method: str, body: str or None, token: str = None):
    response = requests.request(method, url=f"{base_url}:3000{endpoint}",
                                headers={"Content-Type": "application/json",
                                         "Authorization": f"Bearer {token}"},
                                json=body)
    return response.json()
