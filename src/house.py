from profile import Profile
from random import randint
from datetime import datetime
from typing import Dict


class House:
    profile: Profile
    panels_area: float
    people_number: int

    def __init__(self, profile: Profile, panels_area: float, people_number: int) -> None:
        self.profile = profile
        self.panels_area = panels_area
        self.people_number = people_number

    def produce(self, irradiance: float):
        return self.panels_area * (randint(15, 22)/100) * irradiance * 1 / 1000

    def consume(self, temperature: float, time: datetime):
        base_value = self.profile.get_hour_value(temperature, time)
        appliances = base_value * 0.19
        appliances += appliances * 0.4 * self.people_number
        cooking = base_value * 0.40
        cooking += cooking * 0.1 * self.people_number
        water_heating = base_value * 0.15
        water_heating += water_heating * 0.2 * self.people_number
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
