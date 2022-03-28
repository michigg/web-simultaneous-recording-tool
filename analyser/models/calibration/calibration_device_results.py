from typing import List

from models.calibration.calibration_device_result import CalibrationDeviceResult


class CalibrationDeviceResults:
    def __init__(self, calibration_device_results: List[CalibrationDeviceResult], reference_spl: float):
        self.calibration_device_results = calibration_device_results
        self.reference_spl = reference_spl
        self.best = min(calibration_device_results, key=lambda result: result.rmse)
        self.worst = max(calibration_device_results, key=lambda result: result.rmse)