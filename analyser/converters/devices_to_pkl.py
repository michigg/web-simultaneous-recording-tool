import logging
import sys

import pandas as pd

from utils.data_exporter import Exporter
from utils.data_loader import Loader

INPUT_DIR = '/home/michigg/GIT/uni/2021-ma-michael-goetz-data/PensCalibration/Test2/Original'
OUTPUT_DIR = '/home/michigg/GIT/uni/2021-ma-michael-goetz-data/PensCalibration/Test2/Converted'
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


# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)

def main():
    logger.info(f'INPUT_DIR: {INPUT_DIR}')

    devices = Loader.load_analysis_from_json(INPUT_DIR)
    dataframe = devices.get_dba_data_frame_by_raw_data()

    output_path = f'{OUTPUT_DIR}/{OUTPUT_FILE_NAME}-1-aggregated-dbas'
    Exporter.save_as_pickle(f'{output_path}.pkl', dataframe)
    Exporter.save_as_csv(f'{output_path}.csv', dataframe)
    logger.info(f'Saved Raw Dataframe as {output_path}')


if __name__ == '__main__':
    main()
