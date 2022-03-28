import logging
import sys

import pandas as pd

from utils.data_exporter import Exporter
from utils.data_loader import Loader

INPUTS = [
    '/home/michigg/GIT/uni/2021-MA-Michael-Goetz-data/data/BufferSizeInfluence/Pen/Converted/devices-buffer_size_256-1-aggregated-dbas.pkl',
    '/home/michigg/GIT/uni/2021-MA-Michael-Goetz-data/data/BufferSizeInfluence/Pen/Converted/devices-buffer_size_512-1-aggregated-dbas.pkl',
    '/home/michigg/GIT/uni/2021-MA-Michael-Goetz-data/data/BufferSizeInfluence/Pen/Converted/devices-buffer_size_1024-1-aggregated-dbas.pkl',
    '/home/michigg/GIT/uni/2021-MA-Michael-Goetz-data/data/BufferSizeInfluence/Pen/Converted/devices-buffer_size_2048-1-aggregated-dbas.pkl',
    '/home/michigg/GIT/uni/2021-MA-Michael-Goetz-data/data/BufferSizeInfluence/Pen/Converted/devices-buffer_size_4096-1-aggregated-dbas.pkl',
    '/home/michigg/GIT/uni/2021-MA-Michael-Goetz-data/data/BufferSizeInfluence/Pen/Converted/devices-buffer_size_8192-1-aggregated-dbas.pkl',
    '/home/michigg/GIT/uni/2021-MA-Michael-Goetz-data/data/BufferSizeInfluence/Pen/Converted/devices-buffer_size_16384-1-aggregated-dbas.pkl'
]
OUTPUT_DIR = '/home/michigg/GIT/uni/2021-MA-Michael-Goetz-data/data/BufferSizeInfluence/Pen/Converted/'
OUTPUT_FILE_NAME = 'all-devices'

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]:\n %(message)s",
    handlers=[
        logging.FileHandler(f"{OUTPUT_DIR}/{OUTPUT_FILE_NAME}_convert.log", mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)


def main():
    logger.info(f'INPUTS: {INPUTS}')
    logger.info(f'Load Devices Dataframe')
    dataframes = []
    for path in INPUTS:
        dataframes.append(Loader.load_analysis_from_pickle(path))

    logger.info(f'Concat Dataframes')
    df = pd.concat(dataframes,
                   axis=0,
                   join="outer",
                   )
    logger.info(f'Result dataframe')
    logger.info(df)

    output_path = f'{OUTPUT_DIR}/{OUTPUT_FILE_NAME}'
    Exporter.save_as_pickle(f'{output_path}-1-aggregated-dbas.pkl', df)
    Exporter.save_as_csv(f'{output_path}-1-aggregated-dbas.csv', df)
    logger.info(f'Saved Raw Dataframe as {output_path}')


if __name__ == '__main__':
    main()
