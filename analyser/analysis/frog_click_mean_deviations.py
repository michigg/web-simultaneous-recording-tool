"""
Generates Plot of dba values per device per distance
"""
import sys

import pandas as pd

from utils import audio_calcs
from utils.data_loader import Loader

import logging

from utils.output import Output

INPUT_DEVICES = '/home/michigg/GIT/uni/2021-ma-michael-goetz-data/FrogsCalibration/Test2/Converted/devices-1-aggregated-dbas.pkl'
OUTPUT_DIR = '/home/michigg/GIT/uni/2021-ma-michael-goetz-data/FrogsCalibration/Test2/Graphs/ClickMean/BoxPlots'

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

'''
Goal is to test click detection and pen calculations.
'''


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
        f'Deviations Between Frogs By Click Count',
        result,
        file_path=f'{OUTPUT_DIR}/level1',
        file_name=f'clicks'
    )


def plot_frog_sizes(dataframe: pd.DataFrame):
    logger.info(f'plot_frog_sizes')
    result = dataframe.unstack('FrogSize')
    result = result.droplevel(0, axis=1)
    logger.info('plot_frog_sizes: prepared dataframe')
    logger.info(result)
    Output.box_plot(
        f'Deviations Between Frogs By Frog Size',
        result,
        file_path=f'{OUTPUT_DIR}/level1',
        file_name=f'frog_sizes'
    )


def plot_positions(dataframe: pd.DataFrame):
    logger.info(f'plot_positions')
    result = dataframe.unstack('FrogPosition')
    result = result.droplevel(0, axis=1)
    logger.info('plot_positions: prepared dataframe')
    logger.info(result)
    Output.box_plot(
        f'Deviations Between Frogs By Position',
        result,
        file_path=f'{OUTPUT_DIR}/level1',
        file_name=f'positions'
    )


def main():
    clicks_per_device = Loader.load_analysis_from_pickle(INPUT_DEVICES)
    clicks_per_device = audio_calcs.calc_dataframe_click_mean(clicks_per_device)
    logger.info('Prepared Dataframe')
    logger.info(clicks_per_device)
    clicks_per_device = clicks_per_device.unstack('FrogId')
    logger.info('Prepared Dataframe')
    logger.info(clicks_per_device)
    clicks_per_device = clicks_per_device.std(axis=1).to_frame()
    clicks_per_device = clicks_per_device.droplevel('TestIteration')
    clicks_per_device = clicks_per_device.droplevel('WindowingFunction')
    clicks_per_device = clicks_per_device.droplevel('SampleRate')
    clicks_per_device = clicks_per_device.droplevel('BufferSize')
    clicks_per_device = clicks_per_device.droplevel('TestID')
    logger.info('Prepared Dataframe')
    logger.info(clicks_per_device)

    distance_keys = clicks_per_device.index.get_level_values('DistanceKey').unique()
    frog_sizes = clicks_per_device.index.get_level_values('FrogSize').unique()
    frog_positions = clicks_per_device.index.get_level_values('FrogPosition').unique()
    clicks = clicks_per_device.index.get_level_values('Clicks').unique()

    plot_clicks(clicks_per_device)
    plot_positions(clicks_per_device)
    plot_frog_sizes(clicks_per_device)
    for click_count in clicks:
        plot_positions_at_click_count(click_count, clicks_per_device)
        for frog_size in frog_sizes:
            plot_frog_size_by_distance(frog_size, click_count, clicks_per_device)
            plot_frog_size_by_positions(frog_size, click_count, clicks_per_device)
        for frog_size in frog_sizes:
            plot_frog_size_by_distance(frog_size, click_count, clicks_per_device)
            plot_frog_size_by_positions(frog_size, click_count, clicks_per_device)


if __name__ == '__main__':
    main()
