import logging
import sys

from utils.audio_calcs import calc_average_sound_level
from utils.data_exporter import Exporter
from utils.data_loader import Loader

INPUT_CSV = '/home/michigg/GIT/uni/2021-MA-Michael-Goetz-data/data/GroundTruth/Test3/Original/reference.csv'
OUTPUT_DIR = '/home/michigg/GIT/uni/2021-MA-Michael-Goetz-data/data/GroundTruth/Test3/Converted'
OUTPUT_FILE_NAME = 'reference'

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
    logger.info(f'INPUT_CSV: {INPUT_CSV}')
    df = Loader.load_analysis_from_csv(INPUT_CSV, index_col=[0, 1, 2, 3, 4, 5])
    logger.info('Input Dataframe:')
    logger.info(df)

    output_path = f'{OUTPUT_DIR}/{OUTPUT_FILE_NAME}-0-raw'
    Exporter.save_as_pickle(f'{output_path}.pkl', df)
    Exporter.save_as_csv(f'{output_path}.csv', df)
    logger.info(f'Saved Raw Dataframe as {output_path}')

    # Old should not be used anymore df_optimized = df.apply(get_rms, axis=1)
    df_optimized = df.apply(calc_average_sound_level, axis=1)
    df_optimized = df_optimized.unstack('TestIteration')
    # Old should not be used anymore df_optimized = df_optimized.apply(get_rms, axis=1)
    df_optimized = df_optimized.apply(calc_average_sound_level, axis=1)
    output_path = f'{OUTPUT_DIR}/{OUTPUT_FILE_NAME}-3-aggregated-dba'
    Exporter.save_as_pickle(f'{output_path}.pkl', df_optimized)
    Exporter.save_as_csv(f'{output_path}.csv', df_optimized)
    logger.info(f'Saved Optimized Dataframe as {output_path}')


if __name__ == '__main__':
    main()
