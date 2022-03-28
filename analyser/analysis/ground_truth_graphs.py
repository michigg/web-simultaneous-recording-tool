import logging
import sys

from utils.shared_ground_truth_functions import prepare_dataframe, get_deviation_to_reference_per_device
from utils.data_loader import Loader
from utils.output import Output

TEST_NUMBER = 3
INPUT = f'/home/michigg/GIT/uni/2021-MA-Michael-Goetz-data/data/GroundTruth/Test{TEST_NUMBER}/Converted/all-3-aggregated-dba.pkl'
OUTPUT_DIR = f'/home/michigg/GIT/uni/2021-MA-Michael-Goetz-data/data/GroundTruth/Test{TEST_NUMBER}/Graphs'
OUTPUT_FILE_NAME = f'base'

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]:\n %(message)s",
    handlers=[
        logging.FileHandler(f"{OUTPUT_DIR}/{OUTPUT_FILE_NAME}_analyse.log", mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)


def main():
    logger.info(f'INPUT: {INPUT}')
    dataframe = Loader.load_analysis_from_pickle(INPUT)
    dataframe = prepare_dataframe(dataframe)
    logger.info('Cleaned dataframe')
    logger.info(dataframe)

    Output.plot_scatter(
        f"Test {TEST_NUMBER}\nMean In dB(A) Per Device",
        dataframe.T,
        xlabel="Reference Noise Level",
        ylabel="Measured dB(A)",
        file_path=OUTPUT_DIR,
        file_name=f'{OUTPUT_FILE_NAME}-1-mean_per_device'
    )

    reference = dataframe.query('Device=="REFERENCE"')
    devices = dataframe.query('Device!="REFERENCE"')
    logger.info('Reference dataframe')
    logger.info(reference)
    logger.info('Devices dataframe')
    logger.info(devices)
    dataframe = get_deviation_to_reference_per_device(devices, reference)
    logger.info('Deviation dataframe')
    logger.info(dataframe)

    Output.plot_bar(
        f"Test {TEST_NUMBER}\nDeviation In dB(A) Per Device",
        dataframe.T,
        xlabel="Reference Noise Level",
        ylabel="Deviation In dB(A)",
        file_path=OUTPUT_DIR,
        file_name=f'{OUTPUT_FILE_NAME}-2-deviation_per_device'
    )


if __name__ == '__main__':
    main()
