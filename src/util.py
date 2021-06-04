import string
import random
import requests
from socketio.client import Client as SocketClient

base_url = "http://13.84.134.143"


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


def create_socket(namespaces: list[str], token: str = None) -> SocketClient:
    socket = SocketClient(logger=True)
    socket.connect(f"{base_url}:6379", {
                   "authorization": f"Bearer {token}"}, None, namespaces=namespaces)
    return socket