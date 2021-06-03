from datetime import datetime
from typing import Dict, List
from pathlib import Path


class Profile:
    samples: Dict[float, List[float]]

    def __init__(self,  file_path: str) -> None:
        self.samples = {}
        lines = open(Path(file_path).absolute(), 'r').read().split("\n")
        self.samples[5] = [float(x) for x in lines[0].split(',')]
        self.samples[10] = [float(x) for x in lines[1].split(',')]
        self.samples[15] = [float(x) for x in lines[2].split(',')]
        self.samples[25] = [float(x) for x in lines[3].split(',')]
        self.samples[30] = [float(x) for x in lines[4].split(',')]
        self.samples[35] = [float(x) for x in lines[5].split(',')]
        self.samples[40] = [float(x) for x in lines[6].split(',')]

    def get_hour_value(self, temperature: float, now_datetime: datetime) -> float:
        if temperature <= 5:
            prof_temp = 5
        elif temperature <= 10:
            prof_temp = 10
        elif temperature <= 15:
            prof_temp = 15
        elif temperature <= 25:
            prof_temp = 25
        elif temperature <= 30:
            prof_temp = 30
        elif temperature >= 35:
            prof_temp = 35
        else:
            prof_temp = 40

        return self.samples[prof_temp][now_datetime.hour]
