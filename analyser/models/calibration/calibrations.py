from typing import List

import pandas as pd

from models.calibration.calibration import Calibration


class Calibrations:
    def __init__(self):
        self.calibrations: List[Calibration] = []

    def add_calibration(self, calibration: Calibration):
        self.calibrations.append(calibration)

    def best_calibration(self):
        return min(self.calibrations, key=lambda item: item.rmse_worst)

    def get_dataframe(self) -> pd.DataFrame:
        dataframes = []
        for calibration in self.calibrations:
            dataframes.append(calibration.get_dataframe())
        return pd.concat(dataframes)