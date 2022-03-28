import numpy as np
import pandas as pd
import logging

from utils import shared_ground_truth_functions
from models.calibration.calibration_device_result import CalibrationDeviceResult

logger = logging.getLogger(__name__)


def calculate_rmse(deviation_per_device: pd.DataFrame) -> float:
    logger.info('calculate_rmse')
    logger.info(deviation_per_device)
    result = deviation_per_device.apply(lambda row: np.sqrt(np.mean(row ** 2)), axis=1)
    logger.info('deviation_per_device.apply(lambda dbs: np.sqrt(np.mean(dbs ** 2)), axis=1)')
    logger.info(result)
    result = result.mean().round(2)
    logger.info('result.mean().round(2)')
    logger.info(result)
    return result


def get_calibrated_ground_truth(calibration_value_per_device: pd.DataFrame, ground_truth: pd.DataFrame) -> pd.DataFrame:
    calibration_value_per_device_numpy = calibration_value_per_device.to_numpy()
    logger.info('get_calibrated_ground_truth')
    logger.info(calibration_value_per_device_numpy)
    logger.info('get_calibrated_ground_truth: ground_truth')
    logger.info(ground_truth)
    return ground_truth.subtract(calibration_value_per_device_numpy, axis='index')


def get_deviation(reference: pd.DataFrame, data: pd.DataFrame) -> pd.DataFrame:
    logger.info('get_deviation')
    return data.subtract(reference.to_numpy(), axis=1).T


def get_calibration_value(reference_device: float, devices: pd.DataFrame) -> pd.Series:
    return devices.subtract(reference_device)


def get_ground_truth_deviation(ground_truth_all: pd.DataFrame):
    ground_truth_all = shared_ground_truth_functions.prepare_dataframe(ground_truth_all)
    logger.info('Prepared ground truth dataframe')
    logger.info(ground_truth_all)

    reference = ground_truth_all.query('Device=="REFERENCE"')
    devices = ground_truth_all.query('Device!="REFERENCE"')
    deviation = shared_ground_truth_functions.get_deviation_to_reference_per_device(devices_dataframe=devices,
                                                                                    reference_dataframe=reference)
    return deviation, reference, devices


def calculate_calibrated_ground_truth_deviation(reference_spl: float,
                                                calibration_device_value_per_device: pd.DataFrame,
                                                devices_ground_truth: pd.DataFrame,
                                                reference: pd.DataFrame
                                                ) -> pd.DataFrame:
    """
    Calculates the calibrated ground truth deviation.
    This is the deviation between the reference microphone values and the calibrated devices values.

    :param reference_spl: reference value of a virtual calibration device
    :param calibration_device_value_per_device: calibration device value per device
    :param devices_ground_truth: original recorded ground truth values
    :param reference: reference microphone values
    :return: deviation between the reference microphone values and the calibrated devices values
    """
    calibration_value_per_device = get_calibration_value(reference_spl, calibration_device_value_per_device)
    logger.info('calculate_calibrated_deviation: calibration_value_per_device')
    logger.info(reference_spl)
    logger.info(calibration_device_value_per_device)
    logger.info(calibration_value_per_device)

    calibrated_ground_truth = get_calibrated_ground_truth(calibration_value_per_device, devices_ground_truth)
    logger.info('calibrated_ground_truth')
    logger.info(calibrated_ground_truth)
    logger.info('calculate_calibrated_deviation: calibrated_ground_truth')
    logger.info(calibrated_ground_truth)

    return get_deviation(reference, calibrated_ground_truth)


def generate_rmse(
        reference_spl: float,
        devices: pd.DataFrame,
        devices_ground_truth: pd.DataFrame,
        reference: pd.DataFrame,
        calibration_device_id: int
) -> CalibrationDeviceResult:
    logger.info('generate_rmse: start')
    deviation_per_device = calculate_calibrated_ground_truth_deviation(
        reference_spl,
        devices,
        devices_ground_truth,
        reference
    )
    logger.info('deviation_per_device')
    logger.info(deviation_per_device)
    average_error = calculate_rmse(deviation_per_device)
    logger.info('generate_rmse: end')
    return CalibrationDeviceResult(
        original_record=devices,
        calibration_device_id=calibration_device_id,
        rmse=average_error,
        reference_spl=reference_spl,
        deviation=deviation_per_device)
