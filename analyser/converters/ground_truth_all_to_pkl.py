import logging
import sys

import pandas as pd

from utils.data_exporter import Exporter
from utils.data_loader import Loader

INPUT_REFERENCE = '/home/michigg/GIT/uni/2021-MA-Michael-Goetz-data/data/GroundTruth/Test3/Converted/reference-3-aggregated-dba.pkl'
INPUT_DEVICES = '/home/michigg/GIT/uni/2021-MA-Michael-Goetz-data/data/GroundTruth/Test3/Converted/devices-3-aggregated-dba.pkl'
OUTPUT_DIR = '/home/michigg/GIT/uni/2021-MA-Michael-Goetz-data/data/GroundTruth/Test3/Converted'
OUTPUT_FILE_NAME = 'all-3-aggregated-dba'
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
    logger.info(f'INPUT_REFERENCE: {INPUT_REFERENCE}')
    logger.info(f'INPUT_DEVICES: {INPUT_DEVICES}')
    logger.info(f'Load Devices Dataframe')
    df_devices = Loader.load_analysis_from_pickle(INPUT_DEVICES).to_frame()

    logger.info(f'Load reference dataframe')
    df_reference = Loader.load_analysis_from_pickle(INPUT_REFERENCE)
    df_reference = df_reference.to_frame()
    df_reference = pd.concat([df_reference], keys=[0], names=['SampleRate'])
    df_reference = pd.concat([df_reference], keys=[0], names=['BufferSize'])
    df_reference = pd.concat([df_reference], keys=[''], names=['WindowingFunction'])
    df_reference = df_reference.reorder_levels(df_devices.index.names)
    logger.info(f'Optimized dataframe')
    logger.info(df_reference)

    df = pd.concat([df_reference, df_devices],
                   axis=0,
                   join="inner",
                   )
    logger.info(f'Result dataframe')
    logger.info(df)

    output_path = f'{OUTPUT_DIR}/{OUTPUT_FILE_NAME}'
    Exporter.save_as_pickle(f'{output_path}.pkl', df)
    Exporter.save_as_csv(f'{output_path}.csv', df)
    logger.info(f'Saved Dataframe as {output_path}')


if __name__ == '__main__':
    main()
