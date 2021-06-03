from typing import Dict,  Tuple
from datetime import datetime
from pathlib import Path
import csv


class Environment:
    samples: Dict[datetime, Tuple[float, float]]

    def __init__(self, environment_path: str) -> None:
        self.samples = {}

        with open(Path(environment_path).absolute(), 'r') as environment_file:
            reader = csv.reader(environment_file, delimiter=',')
            next(reader)
            for row in reader:
                [_, start, _, temperature, dni] = row
                start_date = datetime.fromisoformat(start[:-1])
                self.samples[start_date] = (float(temperature), float(dni))

    def get_data(self, time: datetime):
        return self.samples[time]

    def get_start_date(self):
        return list(self.samples.keys())[0]

    def get_end_date(self):
        return list(self.samples.keys())[len(self.samples.keys()) - 1]
