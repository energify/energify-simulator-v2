import pickle
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
from environment import Environment
from house import House
import matplotlib.pyplot as plt


class Community:
    name: str
    houses: List[House]
    environment: Environment

    def __init__(self, name: str, environment: Environment) -> None:
        self.name = name
        self.houses = []
        self.environment = environment

    def save(self):
        with open(Path(f"communities/{self.name}.pkl").absolute(), 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

    def add_house(self, house: House) -> None:
        self.houses.append(house)

    def start_simulation(self, interval: int) -> None:
        start = self.environment.get_start_date()
        end = self.environment.get_end_date()

        while start < end:
            temperature, irradiance = self.environment.get_data(start)

            if start.day == 1:
                print(start)

            for house in self.houses:
                house.simulate(start, interval, temperature, irradiance)

            start = datetime.fromtimestamp(start.timestamp() + interval)

    def start_simulation_plot(self, interval: int, plot_x_hours: int) -> None:
        start = self.environment.get_start_date()
        end = self.environment.get_end_date()
        x = []
        houses_y = {}

        while start < end:
            temperature, irradiance = self.environment.get_data(start)

            if (start.timestamp() - 15 * 60) % (plot_x_hours * 3600) == 0:
                print(start)
                x.append(start)

                for house in self.houses:
                    key = str(self.houses.index(house))
                    if key in houses_y:
                        houses_y[key].append(house.simulate(
                            start, interval, temperature, irradiance))
                    else:
                        houses_y[key] = [house.simulate(
                            start, interval, temperature, irradiance)]
            else:
                for house in self.houses:
                    key = str(self.houses.index(house))
                    houses_y[key][len(
                        houses_y[key])-1] += house.simulate(start, interval, temperature, irradiance)

            start = datetime.fromtimestamp(start.timestamp() + interval)

        for house in self.houses:
            key = str(self.houses.index(house))
            plt.plot(x, houses_y[key], label=f"House #{int(key) + 1}, {house}")
            plt.legend(fontsize="x-small")
        plt.show()

    def __str__(self) -> str:
        return f"Houses -> {self.houses} "

    def load(community_path: str):
        with open(Path(community_path).absolute(), 'rb') as input:
            return pickle.load(input)
