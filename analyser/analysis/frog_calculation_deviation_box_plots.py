import sys

import pandas as pd

from analysis.frog_click_mean_calculation import calc_click_mean_quantil_based
from utils import dataframe_index, audio_calcs
from utils.data_loader import Loader

import logging

from utils.output import Output

INPUT_DEVICES = '/home/michigg/GIT/uni/2021-ma-michael-goetz-data/FrogsCalibration/Test2/Converted/devices-1-aggregated-dbas.pkl'
OUTPUT_DIR = '/home/michigg/GIT/uni/2021-ma-michael-goetz-data/FrogsCalibration/Test2/Graphs/Calculations/BoxPlots'

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]:\n %(message)s",
    handlers=[
        logging.FileHandler(f"{OUTPUT_DIR}/analyse.log", mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


def main():
    devices = Loader.load_analysis_from_pickle(INPUT_DEVICES)
    sample_rate = dataframe_index.get_sample_rate(devices)
    buffer_size = dataframe_index.get_buffer_size(devices)
    dataframes = []

    # global max
    result = audio_calcs.calculate_global_max(devices)
    result = result.unstack('FrogId')
    result = result.std(axis=1).to_frame()
    result.columns = ['global max']
    dataframes.append(result)

    # quantil based deviations
    result = devices.apply(
        calc_click_mean_quantil_based,
        axis=1,
        sample_rate=sample_rate,
        buffer_size=buffer_size,
        db_only=True
    ).to_frame()
    result = result.unstack('FrogId')
    result = result.std(axis=1).to_frame()
    result.columns = ['quantile based']
    dataframes.append(result)

    # global max based using db_range
    for db_range in [10, 15, 20]:
        result = devices.apply(
            audio_calcs.calc_series_click_mean,
            axis=1,
            sample_rate=sample_rate,
            buffer_size=buffer_size,
            db_range=db_range,
            return_maxima=False
        ).to_frame()
        result = result.unstack('FrogId')
        result = result.std(axis=1).to_frame()
        result.columns = [f'{db_range} dB(A) range global max']
        dataframes.append(result)

    results = pd.concat(dataframes, axis=1)
    logger.info(results)
    Output.box_plot(
        '',
        # f'Deviations In dB(A) Between Frogs By Calculation Method',
        results,
        file_path=f'{OUTPUT_DIR}',
        file_name=f'box-plot-calculation-methods',
        ignore_clean=True,
        hide_outliers=True
    )


if __name__ == '__main__':
    main()
