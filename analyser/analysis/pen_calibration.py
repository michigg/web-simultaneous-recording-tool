import logging
import sys
import time
from typing import List

import numpy as np
import pandas as pd

from utils.shared_calibration_methods import calculate_rmse, get_ground_truth_deviation, \
    generate_rmse
from models.calibration.calibration_device_result import CalibrationDeviceResult
from models.calibration.calibration_device_results import CalibrationDeviceResults
from models.calibration.rmses_result import RMSESResult
from models.calibration.calibration import Calibration
from models.calibration.calibrations import Calibrations
from utils import dataframe_index, audio_calcs
from utils.data_exporter import Exporter
from utils.data_loader import Loader
from utils.output import Output

GROUND_TRUTH_ID = 3
# INPUT_DEVICES_FROG = '/home/michigg/GIT/uni/2021-ma-michael-goetz-data/PensCalibration/Test1/Converted/devices-1-aggregated-dbas.pkl'
INPUT_DEVICES_PEN = '/home/michigg/GIT/uni/2021-ma-michael-goetz-data/PensCalibration/Test2/Converted/devices-1-aggregated-dbas.pkl'
INPUT_DEVICES_GROUND_TRUTH = f'/home/michigg/GIT/uni/2021-ma-michael-goetz-data/GroundTruth/Test{GROUND_TRUTH_ID}/Converted/all-3-aggregated-dba.pkl'
OUTPUT_DIR = '/home/michigg/GIT/uni/2021-ma-michael-goetz-data/PensCalibration/Test2/Graphs/Calibration'

SETTING_DEVICES = ['REFERENCE',
                   'MOTOG6',
                   'XPERIAZ3',
                   'XPERIAZ3COM',
                   'XPERIAZ3COM2',
                   'ONEPLUS8T',
                   'LENOVOTAB',
                   'LENOVOTAB2',
                   'IPHONE6S',
                   'IPHONE6S2'
                   ]
SETTING_BASE_REFERENCE = 65
SETTING_HIGHEST_REFERENCE = 100

LOG_LEVEL = logging.WARN
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s]:\n %(message)s",
    handlers=[
        logging.FileHandler(f"{OUTPUT_DIR}/analyse.log", mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)

TEST_ITERATION_MAP = {
    1: "SLOW_CLICKS",
    2: "FAST_CLICKS"
}

DISTANCE_MAP = {
    "0m": "0m",
    "MEDIUM_PERSON_SHOULDER_MAX": "SHOULDERS",
    "MEDIUM_PERSON_ARM_MAX": "ARMS"
}

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


def generate_rmses(
        devices: pd.DataFrame,
        devices_ground_truth: pd.DataFrame,
        reference: pd.DataFrame,
        base_reference_spl: float,
        highest_reference_spl,
) -> RMSESResult:
    logger.info('generate_plot_rmse')

    reference_spl_range = highest_reference_spl - base_reference_spl
    logger.info(f'reference_spl_range: {reference_spl_range}')

    results = []
    for i in np.arange(0, reference_spl_range, 0.1):
        logger.info('New Iteration -----------------------------------------------------------------------------')
        reference_spl = (base_reference_spl + i).round(4)
        logger.info(f'reference_spl: {reference_spl}')

        pen_ids = devices.index.get_level_values('PenId').unique()
        logger.info(f'Found Pen Ids: {pen_ids}')
        pens: List[CalibrationDeviceResult] = []
        for pen_id in pen_ids:
            logger.info(f'Pen Id: {pen_id}')
            pen_id_filtered_devices = devices.query(f'PenId==@pen_id')

            result = generate_rmse(
                reference_spl=reference_spl,
                devices=pen_id_filtered_devices,
                devices_ground_truth=devices_ground_truth,
                reference=reference,
                calibration_device_id=pen_id
            )
            pens.append(result)
        results.append(CalibrationDeviceResults(calibration_device_results=pens, reference_spl=reference_spl))
    return RMSESResult(
        devices=devices,
        results=results,
        lowest_reference_spl=base_reference_spl,
        highest_reference_spl=highest_reference_spl
    )


def get_calibrations(
        calc_name: str,
        devices_pens: pd.DataFrame,
        devices_ground_truth: pd.DataFrame,
        reference: pd.DataFrame,
        ground_truth_rmse: float
) -> Calibrations:
    # distance_keys = ["0m"]
    # test_iterations = [1]
    distance_keys = devices_pens.index.get_level_values('DistanceKey').unique()
    logger.info(f'Found Distance Keys: {distance_keys}')
    calibrations = Calibrations()
    for distance_key in distance_keys:
        distance_filtered_devices_pens = devices_pens.query(f'DistanceKey==@distance_key')
        test_iterations = distance_filtered_devices_pens.index.get_level_values('TestIteration').unique()
        logger.info(f'Found Test Iterations: {distance_keys}')
        for test_iteration in test_iterations:
            test_iteration_filtered_devices_pens = distance_filtered_devices_pens.query(
                f'TestIteration==@test_iteration')
            # Calculate pen device value
            logger.info(f'Distance Key: {distance_key}\nTest Iteration: {test_iteration}')
            logger.info(f'test_iteration_filtered_devices_pens')
            logger.info(test_iteration_filtered_devices_pens)

            # Find best possible calibration point
            rmses_result = generate_rmses(
                devices=test_iteration_filtered_devices_pens,
                devices_ground_truth=devices_ground_truth,
                reference=reference,
                base_reference_spl=SETTING_BASE_REFERENCE,
                highest_reference_spl=SETTING_HIGHEST_REFERENCE
            )
            calibrations.add_calibration(Calibration(
                distance_key=distance_key,
                test_iteration=test_iteration,
                clicks=dataframe_index.get_clicks(test_iteration_filtered_devices_pens),
                calc_name=calc_name,
                rmses_result=rmses_result,
                rmse_ground_truth=ground_truth_rmse
            ))
    return calibrations


def generate_output(
        global_max_calibrations: Calibrations,
        click_mean_calibrations: Calibrations,
        use_devices
):
    logger.setLevel(logging.INFO)
    for calibrations in [global_max_calibrations, click_mean_calibrations]:
        best_calibration = calibrations.best_calibration()
        logger.info(f'Best Calibration:\n '
                    f'Calculation Type: {best_calibration.calc_name}\n'
                    f'Best Pen Id: Pen{best_calibration.best_calibration_device_id},\n'
                    f'Worst Pen Id: Pen{best_calibration.worst_calibration_device_id}\n'
                    f'Distance Key: {best_calibration.distance_key}\n'
                    f'Test Iteration: {best_calibration.test_iteration}\n'
                    f'Click Count: {best_calibration.clicks}\n'
                    f'Reference: {best_calibration.reference_calibration_device_spl} dB(A)\n'
                    )
        Exporter.save_as_csv(
            f'{OUTPUT_DIR}/{best_calibration.calc_name}-calibrations.csv',
            calibrations.get_dataframe()
        )
        best_calibration_info = f'Pen{best_calibration.worst_calibration_device_id}, ' \
                                f'Distance: {DISTANCE_MAP[best_calibration.distance_key]}, ' \
                                f'Clicks: {best_calibration.clicks}, ' \
                                f'Calculation: {best_calibration.calc_name}, ' \
                                f'Reference: {best_calibration.reference_calibration_device_spl} dB(A)'
        logger.info(f'best_calibration_info: {best_calibration_info}')
        f_devices = "".join([elem[:1] for elem in use_devices])
        # base_file_name = f'gt{GROUND_TRUTH_ID}-ti_{test_iteration}-di_{distance_key.lower()}-de_{f_devices}'
        base_file_name = f'{best_calibration.calc_name}-best_calibration'
        file_path = f'{OUTPUT_DIR}'
        plot_info = f'Using: Ground Truth {GROUND_TRUTH_ID}; Devices: {f_devices}'
        logger.info(f'Used Plot Info: {plot_info}')
        logger.info(f'Used Base File Name: {base_file_name}')
        logger.info(f'Used File Path: {file_path}')

        # Output.plot_scatter(
        #     f'Recorded dB(A) Values Of \n{best_calibration_info}\n{plot_info}',
        #     best_calibration.best_result.worst.original_record
        #         .droplevel('PenId')
        #         .droplevel('PenBrand')
        #         .droplevel('SampleRate')
        #         .droplevel('BufferSize')
        #         .droplevel('TestIteration')
        #         .droplevel('Clicks')
        #         .droplevel('WindowingFunction')
        #         .droplevel('DistanceKey')
        #         .droplevel('TestID').T,
        #     xlabel='Noise Preset in dB(A)',
        #     ylabel='Deviation in dB(A)',
        #     file_path=file_path,
        #     file_name=f'{base_file_name}-1-dbas'
        # )

        rmses_dataframe = pd.DataFrame(
            [{"error": result.worst.rmse} for result in best_calibration.rmses_result.results])
        rmses_dataframe.index = [result.reference_spl for result in best_calibration.rmses_result.results]
        Output.plot_scatter(
            '',
            # f'Root Mean Squares\nUsed Reference Pens From {best_calibration.lowest_reference_spl} dB(A) To {best_calibration.highest_reference_spl} dB(A)\n{best_calibration_info}\n{plot_info}',
            rmses_dataframe,
            xlabel='Used reference sound pressure level in dB(A)',
            ylabel='Root Mean Square Error',
            file_path=file_path,
            file_name=f'{base_file_name}-3-rmses'
        )

        Output.plot_bar(
            '',
            # f'Best Reference Deviation\nRMSE (Before/Now): {best_calibration.rmse_ground_truth}/{best_calibration.rmse_worst}\n{best_calibration_info}\n{plot_info}',
            best_calibration.worst_deviation,
            xlabel='Noise Preset in dB(A)',
            ylabel='Deviation in dB(A)',
            file_path=file_path,
            file_name=f'{base_file_name}-4-calibrated_deviation-{"better" if best_calibration.rmse_is_better_than_ground_truth_rmse() else "worse"}'
        )
    logger.setLevel(LOG_LEVEL)


def main():
    start_time = time.time()
    use_devices = SETTING_DEVICES
    use_noise_presets = ['40_DBA', '45_DBA', '50_DBA', '55_DBA', '60_DBA', '65_DBA', '70_DBA', '75_DBA', '80_DBA',
                         '85_DBA', '90_DBA']
    # use_noise_presets = ['50_DBA', '55_DBA', '60_DBA', '65_DBA', '70_DBA', '75_DBA', '80_DBA']
    # use_noise_presets = ['50_DBA', '55_DBA', '60_DBA']

    logger.info('Pen Calibration')
    # Ground Truth Data
    devices_ground_truth = Loader.load_analysis_from_pickle(INPUT_DEVICES_GROUND_TRUTH)
    devices_ground_truth.sort_index(axis=0, inplace=True)
    devices_ground_truth = devices_ground_truth.query(f'Device==@use_devices and ConfigNoisePreset==@use_noise_presets')

    ground_truth_deviation, reference, devices_ground_truth = get_ground_truth_deviation(devices_ground_truth)
    logger.info('ground_truth_deviation')
    logger.info(ground_truth_deviation)
    ground_truth_rmse = calculate_rmse(ground_truth_deviation)
    logger.info(f'base_deviation: rmse: {ground_truth_rmse}')

    # Pen Data
    devices_pens = Loader.load_analysis_from_pickle(INPUT_DEVICES_PEN)
    devices_pens.sort_index(axis=0, inplace=True)
    devices_pens = devices_pens.query(f'Device==@use_devices')
    logger.info(devices_pens)

    global_max_pens = audio_calcs.calculate_global_max(devices_pens)
    logger.info("Using global max calcuation")
    logger.info(global_max_pens)

    global_max_calibrations = get_calibrations(
        calc_name="global_max",
        devices_pens=global_max_pens,
        devices_ground_truth=devices_ground_truth,
        reference=reference,
        ground_truth_rmse=ground_truth_rmse
    )

    db_range = 10
    click_mean_pens = audio_calcs.calc_dataframe_click_mean(devices_pens, db_range)
    click_mean_calibrations = get_calibrations(
        calc_name="click_mean",
        devices_pens=click_mean_pens,
        devices_ground_truth=devices_ground_truth,
        reference=reference,
        ground_truth_rmse=ground_truth_rmse
    )
    generate_output(
        global_max_calibrations=global_max_calibrations,
        click_mean_calibrations=click_mean_calibrations,
        use_devices=use_devices
    )
    end_time = time.time()
    logger.setLevel(logging.INFO)
    logger.info(f'Elapsed Time: {end_time - start_time}')
    logger.setLevel(LOG_LEVEL)


if __name__ == '__main__':
    main()
