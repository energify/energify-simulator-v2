from profile import Profile
from random import randint
from datetime import datetime
from util import base_url,  generate_email, generate_word, request
from socketio import Client as SocketClient


class House:
    profile: Profile
    socket: SocketClient
    bearer_token: str
    email: str
    password: str
    panels_area: float
    panel_efficiency: float
    people_number: int

    def __init__(self, profile: Profile, panels_area: float, people_number: int) -> None:
        self.bearer_token = ""
        self.email = ""
        self.password = ""
        self.panel_efficiency = randint(15, 22) / 100
        self.profile = profile
        self.panels_area = panels_area
        self.people_number = people_number

    def register(self):
        self.email = generate_email()
        self.password = generate_word(8)
        payload = {
            'email': self.email,
            'password': self.password,
            'name': self.password,
            'hederaAccountId': generate_word(8)
        }
        response = request('/auth/register', "POST", payload)
        print(f"House {response['email']} registered")

    def login(self):
        payload = {'email': self.email, 'password': self.password}
        response = request('/auth/login', "POST", payload, self.bearer_token)
        self.bearer_token = response["accessToken"]
        print(f"House {self.email} logged in")

    def set_prices(self, buy_price: float, sell_price: float):
        payload = {'buyPrice': buy_price, 'sellPrice': sell_price}
        request("/users/prices", "PUT", payload, self.bearer_token)
        print(f"House {self.email} set prices")

    def establish_connection(self):
        self.socket = SocketClient()
        self.socket.connect(f"{base_url}:6379", headers={
            "authorization": f"{self.bearer_token}"}, namespaces=["", "/measures"])

        print(f"House {self.email} sid is {self.socket.sid}")

    def notify_measure(self, measure: float, time: datetime):
        self.socket.emit("store", data={'value': measure, 'timestamp': time.timestamp()},
                         namespace='/measures')

    def produce(self, irradiance: float):
        return self.panels_area * self.panel_efficiency * irradiance * 1 / 1000

    def consume(self, temperature: float, time: datetime):
        base_value = self.profile.get_hour_value(temperature, time)
        appliances = base_value * 0.19
        appliances += appliances * 0.4 * (self.people_number - 1)
        cooking = base_value * 0.40
        cooking += cooking * 0.1 * (self.people_number - 1)
        water_heating = base_value * 0.15
        water_heating += water_heating * 0.2 * (self.people_number - 1)
        air_conditioning = base_value * 0.05
        space_heating = base_value * 0.21

        return appliances + cooking + water_heating + air_conditioning + space_heating

    def simulate(self, time: datetime, interval: int, temperature: float, irradiance: float):
        consumed = self.consume(temperature, time)
        produced = self.produce(irradiance)
        return interval / 3600 * (produced - consumed)

    def __str__(self) -> str:
        return f"People --> {self.people_number}, Panels Area -> {self.panels_area}\n"

    def __repr__(self) -> str:
        return f"People --> {self.people_number}, Panels Area -> {self.panels_area}\n"
