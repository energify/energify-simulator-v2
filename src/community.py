import pickle
from datetime import datetime
from pathlib import Path
from typing import List, Tuple
from house import House
import csv
import matplotlib.pyplot as plt


class Community:
    name: str
    houses: List[House]
    environment_data: List[Tuple[datetime, datetime, float, float]]

    def __init__(self, name: str, environment_path: str) -> None:
        self.name = name
        self.houses = []
        self.environment_data = []

        with open(Path(environment_path).absolute(), 'r') as environment_file:
            reader = csv.reader(environment_file, delimiter=',')
            next(reader)
            for row in reader:
                [end, start, _, temperature, dni] = row
                self.environment_data.append(
                    [datetime.fromisoformat(start[:-1]), datetime.fromisoformat(end[:-1]), float(temperature), float(dni)])

    def save(self):
        with open(Path(f"communities/{self.name}.pkl").absolute(), 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

    def add_house(self, house: House) -> None:
        self.houses.append(house)

    def get_temp_dni(self, time: datetime) -> Tuple[float, float]:
        for [start, end, temperature, dni] in self.environment_data:
            if time >= start and time <= end:
                return [temperature, dni]

    def start_simulation(self, interval: int) -> None:
        start, *_ = self.environment_data[0]
        _, end, *_ = self.environment_data[len(self.environment_data)-1]

        while start < end:
            temperature, irradiance = self.get_temp_dni(start)

            for house in self.houses:
                house.simulate(start, interval, temperature, irradiance)

            start = datetime.fromtimestamp(start.timestamp() + interval)

    def show_simulation(self, interval: int) -> None:
        start, *_ = self.environment_data[0]
        nex = datetime.fromtimestamp(start.timestamp() + interval)
        _, end, *_ = self.environment_data[len(self.environment_data)-1]

        x = []
        y_values = {}

        while nex < end:
            for house in self.houses:
                kwh = house.get_kwh(start, nex)
                key = str(self.houses.index(house))

                if key not in y_values:
                    y_values[key] = [kwh]
                else:
                    y_values[key].append(kwh)

            x.append(start)
            start = nex
            nex = datetime.fromtimestamp(start.timestamp() + interval)

        for house in self.houses:
            key = str(self.houses.index(house))
            plt.plot(x, y_values[key], label=f"House #{int(key) + 1}, {house}")
            plt.legend(fontsize="x-small")
        plt.show()

    def __str__(self) -> str:
        return f"Houses -> {self.houses} "

    def load(community_path: str):
        with open(Path(community_path).absolute(), 'rb') as input:
            return pickle.load(input)
