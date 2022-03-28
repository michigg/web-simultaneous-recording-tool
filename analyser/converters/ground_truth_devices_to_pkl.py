import logging
import sys

import pandas as pd

from utils.audio_calcs import get_index_of_bin_at_x_milliseconds_from_first, \
    get_index_of_bin_at_x_milliseconds_from_last, calc_average_sound_level
from utils.data_exporter import Exporter
from utils.data_loader import Loader

INPUT_DIR = '/home/michigg/GIT/uni/2021-ma-michael-goetz-data/GroundTruth/Test1/Original/Smartphones'
OUTPUT_DIR = '/home/michigg/GIT/uni/2021-ma-michael-goetz-data/GroundTruth/Test1/Converted'
OUTPUT_FILE_NAME = 'devices'

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]:\n %(message)s",
    handlers=[
        logging.FileHandler(f"{OUTPUT_DIR}/{OUTPUT_FILE_NAME}_convert.log", mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


def get_shortened_dataframe(dataframe: pd.DataFrame, first_milliseconds: int, last_milliseconds: int) -> pd.DataFrame:
    logger.info(f'get_shortened_dataframe')
    columns = dataframe.shape[1]

    sample_rate = dataframe.index.get_level_values('SampleRate').unique()
    if len(sample_rate) != 1:
        logger.error(f'Different sample rates found: {sample_rate}')
        raise Exception(f'Different sample rates found: {sample_rate}')
    sample_rate = int(sample_rate[0])

    buffer_size = dataframe.index.get_level_values('BufferSize').unique()
    if len(buffer_size) != 1:
        logger.error(f'Different buffer sizes found: {buffer_size}')
        raise Exception(f'Different buffer sizes found: {buffer_size}')
    buffer_size = int(buffer_size[0])

    logger.info(f'Used Sample Rate: {sample_rate}')
    logger.info(f'Used Buffer Size: {buffer_size}')

    from_bin_id = get_index_of_bin_at_x_milliseconds_from_first(first_milliseconds, sample_rate, buffer_size)
    to_bin_id = columns - get_index_of_bin_at_x_milliseconds_from_last(last_milliseconds, sample_rate, buffer_size)

    logger.info(f'Used Borders: From: {from_bin_id}; To: {to_bin_id}')
    return dataframe.iloc[:, from_bin_id:to_bin_id]


def main():
    logger.info(f'INPUT_DIR: {INPUT_DIR}')

    devices = Loader.load_analysis_from_json(INPUT_DIR)
    dataframe = devices.get_dba_data_frame_by_raw_data()
    logger.info(f'Input Dataframe')
    logger.info(dataframe)

    output_path = f'{OUTPUT_DIR}/{OUTPUT_FILE_NAME}-1-aggregated-dbas'
    Exporter.save_as_pickle(f'{output_path}.pkl', dataframe)
    Exporter.save_as_csv(f'{output_path}.csv', dataframe)
    logger.info(f'Saved Raw Dataframe as {output_path}')

    start_milliseconds = 1000
    stop_milliseconds = 0
    logger.info(f'Cut dataframe at {start_milliseconds} milliseconds from start')
    logger.info(f'Cut dataframe at {stop_milliseconds} milliseconds from end')
    shortened_dataframe = get_shortened_dataframe(dataframe, start_milliseconds, stop_milliseconds)
    logger.info(f'Shortened Dataframe')
    logger.info(shortened_dataframe)

    shortened_dataframe = shortened_dataframe.apply(calc_average_sound_level, axis=1)
    logger.info(f'Shortened Dataframe with average total sound level')
    logger.info(shortened_dataframe)
    shortened_dataframe = shortened_dataframe.unstack('TestIteration')
    logger.info(f'Shortened Dataframe with average total sound level unstacked')
    logger.info(shortened_dataframe)

    output_path = f'{OUTPUT_DIR}/{OUTPUT_FILE_NAME}-2-aggregated-dba_per_test_iteration'
    Exporter.save_as_pickle(f'{output_path}.pkl', shortened_dataframe)
    Exporter.save_as_csv(f'{output_path}.csv', shortened_dataframe)
    logger.info(f'Saved Raw Dataframe as {output_path}')

    shortened_dataframe = shortened_dataframe.apply(calc_average_sound_level, axis=1)
    logger.info(f'Shortened Dataframe with average total sound level over test iterations')
    logger.info(shortened_dataframe)

    output_path = f'{OUTPUT_DIR}/{OUTPUT_FILE_NAME}-3-aggregated-dba'
    Exporter.save_as_pickle(f'{output_path}.pkl', shortened_dataframe)
    Exporter.save_as_csv(f'{output_path}.csv', shortened_dataframe)
    logger.info(f'Saved Raw Dataframe as {output_path}')


if __name__ == '__main__':
    main()
