import pandas as pd

from models.calibration.rmses_result import RMSESResult


class Calibration:
    def __init__(self,
                 distance_key: str,
                 test_iteration: int,
                 clicks: int,
                 calc_name: str,
                 rmses_result: RMSESResult,
                 rmse_ground_truth: float
                 ):
        self.distance_key = distance_key
        self.test_iteration = test_iteration
        self.clicks = clicks
        self.calc_name = calc_name
        self.rmses_result = rmses_result
        self.best_result = rmses_result.best_result()
        self.rmse_ground_truth = rmse_ground_truth
        self.rmse_worst = self.best_result.worst.rmse
        self.lowest_reference_spl = rmses_result.lowest_reference_spl
        self.highest_reference_spl = rmses_result.highest_reference_spl
        self.best_calibration_device_id = self.best_result.best.calibration_device_id
        self.worst_calibration_device_id = self.best_result.worst.calibration_device_id
        self.reference_calibration_device_spl = self.best_result.reference_spl
        self.worst_deviation = self.best_result.worst.deviation
        self.best_deviation = self.best_result.best.deviation

    def rmse_is_better_than_ground_truth_rmse(self):
        return self.rmse_ground_truth > self.best_result.worst.rmse

    def rmse_improvement(self):
        return self.rmse_ground_truth - self.best_result.worst.rmse

    def _to_dict(self):
        return {
            "rmse_ground_truth": self.rmse_ground_truth,
            "rmse": self.rmse_worst,
            "lowest_reference_spl": self.lowest_reference_spl,
            "highest_reference_spl": self.highest_reference_spl,
            "best_calibration_device_id": self.best_calibration_device_id,
            "worst_calibration_device_id": self.worst_calibration_device_id,
            "reference_calibration_device_spl": self.reference_calibration_device_spl,
        }

    def _get_multi_index(self):
        multi_index_tuples = (self.distance_key, self.test_iteration, self.clicks, self.calc_name)
        multi_index_names = ["DistanceKey", "TestIteration", "Clicks", "CalcName"]
        return pd.MultiIndex.from_tuples([multi_index_tuples], names=multi_index_names)

    def get_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame([self._to_dict()], index=self._get_multi_index())