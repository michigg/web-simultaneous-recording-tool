import logging
import sys
import time
from typing import List

import numpy as np
import pandas as pd

from utils.shared_calibration_methods import calculate_rmse, get_ground_truth_deviation, generate_rmse
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
INPUT_DEVICES_FROG = '/home/michigg/GIT/uni/2021-ma-michael-goetz-data/FrogsCalibration/Test2/Converted/devices-1-aggregated-dbas.pkl'
INPUT_DEVICES_GROUND_TRUTH = f'/home/michigg/GIT/uni/2021-ma-michael-goetz-data/GroundTruth/Test{GROUND_TRUTH_ID}/Converted/all-3-aggregated-dba.pkl'
OUTPUT_DIR = '/home/michigg/GIT/uni/2021-ma-michael-goetz-data/FrogsCalibration/Test2/Graphs/Calibration'

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
SETTING_HIGHEST_REFERENCE = 110

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

DISTANCE_MAP = {
    "0m": "0m",
    "MEDIUM_PERSON_SHOULDER_MAX": "SHOULDERS",
    "MEDIUM_PERSON_ARM_MAX": "ARMS"
}

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


class FrogCalibration(Calibration):
    def __init__(
            self,
            distance_key: str,
            test_iteration: int,
            clicks: int,
            calc_name: str,
            frog_size: str,
            frog_position: str,
            rmses_result: RMSESResult,
            rmse_ground_truth: float
    ):
        super().__init__(distance_key, test_iteration, clicks, calc_name, rmses_result, rmse_ground_truth)
        self.frog_size = frog_size
        self.frog_position = frog_position

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
        multi_index_tuples = (
            self.distance_key, self.test_iteration, self.clicks, self.calc_name, self.frog_size, self.frog_position)
        multi_index_names = ["DistanceKey", "TestIteration", "Clicks", "CalcName", "FrogSize", "FrogPosition"]
        return pd.MultiIndex.from_tuples([multi_index_tuples], names=multi_index_names)

    def get_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame([self._to_dict()], index=self._get_multi_index())


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

        frog_ids = devices.index.get_level_values('FrogId').unique()
        logger.info(f'Found Frog Ids: {frog_ids}')
        frogs: List[CalibrationDeviceResult] = []
        for frog_id in frog_ids:
            logger.info(f'Frog Id: {frog_id}')
            frog_id_filtered_devices = devices.query(f'FrogId==@frog_id')

            result = generate_rmse(
                reference_spl=reference_spl,
                devices=frog_id_filtered_devices,
                devices_ground_truth=devices_ground_truth,
                reference=reference,
                calibration_device_id=frog_id
            )
            frogs.append(result)
        results.append(CalibrationDeviceResults(calibration_device_results=frogs, reference_spl=reference_spl))
    return RMSESResult(
        devices=devices,
        results=results,
        lowest_reference_spl=base_reference_spl,
        highest_reference_spl=highest_reference_spl
    )


def get_calibrations(
        calc_name: str,
        devices_frogs: pd.DataFrame,
        devices_ground_truth: pd.DataFrame,
        reference: pd.DataFrame,
        ground_truth_rmse: float
) -> Calibrations:
    # distance_keys = ["0m"]
    # test_iterations = [1]
    # frog_sizes = ["SMALL"]
    # frog_positions = ["OPEN_THUMB"]
    distance_keys = devices_frogs.index.get_level_values('DistanceKey').unique()
    logger.info(f'Found Distance Keys: {distance_keys}')
    calibrations = Calibrations()
    for distance_key in distance_keys:
        distance_filtered_devices_frogs = devices_frogs.query(f'DistanceKey==@distance_key')
        test_iterations = distance_filtered_devices_frogs.index.get_level_values('TestIteration').unique()
        logger.info(f'Found Test Iterations: {distance_keys}')
        for test_iteration in test_iterations:
            test_iteration_filtered_devices_frogs = distance_filtered_devices_frogs.query(
                f'TestIteration==@test_iteration')
            frog_sizes = test_iteration_filtered_devices_frogs.index.get_level_values('FrogSize').unique()
            logger.info(f'Found Frog Sizes: {frog_sizes}')
            for frog_size in frog_sizes:
                frog_size_filtered_devices_frogs = test_iteration_filtered_devices_frogs.query(f'FrogSize==@frog_size')
                frog_positions = frog_size_filtered_devices_frogs.index.get_level_values('FrogPosition').unique()
                logger.info(f'Found Frog Positions: {frog_positions}')
                for frog_position in frog_positions:
                    frog_position_filtered_devices_frogs = frog_size_filtered_devices_frogs.query(
                        f'FrogPosition==@frog_position')
                    # Calculate frog device value
                    logger.info(
                        f'Distance Key: {distance_key}\nTest Iteration: {test_iteration}\nFrog Size: {frog_size}\nFrog Position: {frog_position}')
                    logger.info(f'frog_position_filtered_devices_frogs')
                    logger.info(frog_position_filtered_devices_frogs)

                    # Find best possible calibration point
                    rmses_result = generate_rmses(
                        devices=frog_position_filtered_devices_frogs,
                        devices_ground_truth=devices_ground_truth,
                        reference=reference,
                        base_reference_spl=SETTING_BASE_REFERENCE,
                        highest_reference_spl=SETTING_HIGHEST_REFERENCE
                    )
                    calibrations.add_calibration(FrogCalibration(
                        distance_key=distance_key,
                        test_iteration=test_iteration,
                        clicks=dataframe_index.get_clicks(frog_position_filtered_devices_frogs),
                        calc_name=calc_name,
                        frog_size=frog_size,
                        frog_position=frog_position,
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
        best_calibration: FrogCalibration = calibrations.best_calibration()
        logger.info(f'Best Calibration:\n '
                    f'Calculation Type: {best_calibration.calc_name}\n'
                    f'Best Frog Id: Frog{best_calibration.best_calibration_device_id},\n'
                    f'Worst Frog Id: Frog{best_calibration.worst_calibration_device_id}\n'
                    f'Distance Key: {best_calibration.distance_key}\n'
                    f'Test Iteration: {best_calibration.test_iteration}\n'
                    f'Click Count: {best_calibration.clicks}\n'
                    f'Frog Size: {best_calibration.frog_size}\n'
                    f'Frog Position: {best_calibration.frog_position}\n'
                    f'Reference: {best_calibration.reference_calibration_device_spl} dB(A)\n'
                    )
        Exporter.save_as_csv(
            f'{OUTPUT_DIR}/{best_calibration.calc_name}-calibrations.csv',
            calibrations.get_dataframe()
        )
        best_calibration_info = f'Frog{best_calibration.worst_calibration_device_id}, ' \
                                f'Distance: {DISTANCE_MAP[best_calibration.distance_key]}, ' \
                                f'Clicks: {best_calibration.clicks}, ' \
                                f'Calculation: {best_calibration.calc_name},\n' \
                                f'Frog Size: {best_calibration.frog_size}, ' \
                                f'Frog Position: {best_calibration.frog_position}, ' \
                                f'Reference: {best_calibration.reference_calibration_device_spl} dB(A)'
        logger.info(f'best_calibration_info: {best_calibration_info}')
        f_devices = "".join([elem[:1] for elem in use_devices])
        # base_file_name = f'gt{GROUND_TRUTH_ID}-ti_{test_iteration}-di_{distance_key.lower()}-de_{f_devices}'
        base_file_name = f'{best_calibration.calc_name}-best_calibration'
        file_path = f'{OUTPUT_DIR}'
        plot_info = f'Ground Truth {GROUND_TRUTH_ID}; Devices: {f_devices}'
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
            # f'Root Mean Squares\nUsed Reference Frogs From {best_calibration.lowest_reference_spl} dB(A) To {best_calibration.highest_reference_spl} dB(A)\n{best_calibration_info}\n{plot_info}',
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

    logger.info('Frog Calibration')
    # Ground Truth Data
    devices_ground_truth = Loader.load_analysis_from_pickle(INPUT_DEVICES_GROUND_TRUTH)
    devices_ground_truth.sort_index(axis=0, inplace=True)
    devices_ground_truth = devices_ground_truth.query(f'Device==@use_devices and ConfigNoisePreset==@use_noise_presets')

    ground_truth_deviation, reference, devices_ground_truth = get_ground_truth_deviation(devices_ground_truth)
    logger.info('ground_truth_deviation')
    logger.info(ground_truth_deviation)
    ground_truth_rmse = calculate_rmse(ground_truth_deviation)
    logger.info(f'base_deviation: rmse: {ground_truth_rmse}')

    # Frog Data
    devices_frogs = Loader.load_analysis_from_pickle(INPUT_DEVICES_FROG)
    devices_frogs.sort_index(axis=0, inplace=True)
    devices_frogs = devices_frogs.query(f'Device==@use_devices')
    logger.info(devices_frogs)

    global_max_frogs = audio_calcs.calculate_global_max(devices_frogs)
    logger.info("Using global max calcuation")
    logger.info(global_max_frogs)

    global_max_calibrations = get_calibrations(
        calc_name="global_max",
        devices_frogs=global_max_frogs,
        devices_ground_truth=devices_ground_truth,
        reference=reference,
        ground_truth_rmse=ground_truth_rmse
    )

    db_range = 10
    click_mean_frogs = audio_calcs.calc_dataframe_click_mean(devices_frogs, db_range)
    click_mean_calibrations = get_calibrations(
        calc_name="click_mean",
        devices_frogs=click_mean_frogs,
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
