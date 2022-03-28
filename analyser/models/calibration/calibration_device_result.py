import pandas as pd


class CalibrationDeviceResult:
    def __init__(self, original_record: pd.DataFrame, calibration_device_id: int, rmse: float, reference_spl: float,
                 deviation: pd.DataFrame):
        self.original_record = original_record
        self.calibration_device_id = calibration_device_id
        self.rmse = rmse
        self.reference_spl = reference_spl
        self.deviation = deviation