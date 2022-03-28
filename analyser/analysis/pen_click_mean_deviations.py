"""
Generates Plot of dba values per device per distance
"""
import sys

import pandas as pd

from utils import audio_calcs
from utils.data_loader import Loader

import logging

from utils.output import Output

INPUT_DEVICES = '/home/michigg/GIT/uni/2021-ma-michael-goetz-data/PensCalibration/Test2/Converted/devices-1-aggregated-dbas.pkl'
OUTPUT_DIR = '/home/michigg/GIT/uni/2021-ma-michael-goetz-data/PensCalibration/Test2/Graphs/ClickMean/BoxPlots'

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


def clean_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    logger.info('clean_dataframe: start')
    new_dataframe = dataframe.droplevel('TestID')
    new_dataframe = new_dataframe.droplevel('WindowingFunction')
    new_dataframe = new_dataframe.droplevel('TestIteration')
    new_dataframe = new_dataframe.droplevel('DistanceKey')
    logger.info('clean_dataframe: done')
    logger.info(new_dataframe)
    return new_dataframe


# Level 2 Aggregation
def plot_frog_size_by_distance(frog_size: str, clicks: int, dataframe: pd.DataFrame):
    logger.info(f'plot_frog_size: frog_size: {frog_size}')
    logger.info(f'plot_frog_size: clicks: {clicks}')
    result = dataframe.query('FrogSize==@frog_size and Clicks==@clicks')
    result = result.droplevel('FrogSize')
    result = result.unstack('DistanceKey')
    result = result.droplevel(0, axis=1)
    logger.info('Prepared Dataframe')
    logger.info(result)
    Output.box_plot(
        f'Deviations Between Frogs By Distance\nFrog Size {frog_size} Clicks {clicks}',
        result,
        file_path=f'{OUTPUT_DIR}',
        file_name=f'distance-frog_size_{frog_size}-clicks_{clicks}'
    )


def plot_frog_size_by_positions(frog_size: str, clicks: int, dataframe: pd.DataFrame):
    logger.info(f'plot_frog_size: frog_size: {frog_size}')
    logger.info(f'plot_frog_size: clicks: {clicks}')
    result = dataframe.query('FrogSize==@frog_size and Clicks==@clicks')
    result = result.droplevel('FrogSize')
    result = result.unstack('FrogPosition')
    result = result.droplevel(0, axis=1)
    logger.info('Prepared Dataframe')
    logger.info(result)
    Output.box_plot(
        f'Deviations Between Frogs By Position\nFrog Size {frog_size} Clicks {clicks}',
        result,
        file_path=f'{OUTPUT_DIR}',
        file_name=f'position-frog_size_{frog_size}-clicks_{clicks}'
    )


def plot_positions_at_click_count(clicks: int, dataframe: pd.DataFrame):
    logger.info(f'plot_frog_size: clicks: {clicks}')
    result = dataframe.query('Clicks==@clicks')
    result = result.unstack('FrogPosition')
    result = result.droplevel(0, axis=1)
    logger.info('Prepared Dataframe')
    logger.info(result)
    Output.box_plot(
        f'Deviations Between Frogs By Position\nClicks {clicks}',
        result,
        file_path=f'{OUTPUT_DIR}',
        file_name=f'position-clicks_{clicks}'
    )


# Level 1 Aggregation
def plot_clicks(dataframe: pd.DataFrame):
    logger.info(f'plot_clicks')
    result = dataframe.unstack('Clicks')
    result = result.droplevel(0, axis=1)
    logger.info('plot_clicks: prepared dataframe')
    logger.info(result)
    Output.box_plot(
        f'Deviations In dB(A) Between Pens By Click Count',
        result,
        file_path=f'{OUTPUT_DIR}/level1',
        file_name=f'clicks'
    )


def plot_distances(dataframe: pd.DataFrame):
    logger.info(f'plot_distances')
    result = dataframe.unstack('DistanceKey')
    result = result.droplevel(0, axis=1)
    logger.info('plot_distances: prepared dataframe')
    logger.info(result)
    Output.box_plot(
        f'Deviations In dB(A) Between Pens By Distance',
        result,
        file_path=f'{OUTPUT_DIR}/level1',
        file_name=f'distances'
    )


def main():
    devices = Loader.load_analysis_from_pickle(INPUT_DEVICES)
    devices = audio_calcs.calc_dataframe_click_mean(devices)
    logger.info('Prepared Dataframe')
    logger.info(devices)
    devices = devices.unstack('PenId')
    logger.info('Prepared Dataframe')
    logger.info(devices)
    devices = devices.std(axis=1).to_frame()
    devices = devices.droplevel('TestIteration')
    devices = devices.droplevel('WindowingFunction')
    devices = devices.droplevel('SampleRate')
    devices = devices.droplevel('BufferSize')
    devices = devices.droplevel('TestID')
    devices = devices.droplevel('PenBrand')
    logger.info('Prepared Dataframe')
    logger.info(devices)

    distance_keys = devices.index.get_level_values('DistanceKey').unique()
    clicks = devices.index.get_level_values('Clicks').unique()

    plot_clicks(devices)
    plot_distances(devices)


if __name__ == '__main__':
    main()
