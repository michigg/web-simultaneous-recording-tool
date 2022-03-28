from typing import List

import pandas as pd

from models.calibration.calibration_device_results import CalibrationDeviceResults


class RMSESResult:
    def __init__(self,
                 devices: pd.DataFrame,
                 results: List[CalibrationDeviceResults],
                 lowest_reference_spl: float,
                 highest_reference_spl: float
                 ):
        self.devices = devices
        self.results: List[CalibrationDeviceResults] = results
        self.lowest_reference_spl = lowest_reference_spl
        self.highest_reference_spl = highest_reference_spl

    def best_result(self) -> CalibrationDeviceResults:
        return min(self.results, key=lambda item: item.worst.rmse)