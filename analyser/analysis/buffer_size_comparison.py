import logging
import sys

from utils import dataframe_index
from utils.data_loader import Loader
from utils.output import Output

SETTING_DEVICES = ['ONEPLUS8T', 'XPERIAZ3COM']
INPUT = f'/home/michigg/GIT/uni/2021-ma-michael-goetz-data/BufferSizeInfluence/Pen/Converted/all-devices-1-aggregated-dbas.pkl'
OUTPUT_DIR = f'/home/michigg/GIT/uni/2021-ma-michael-goetz-data/BufferSizeInfluence/Pen/Graphs/RecodingComparison'

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]:\n %(message)s",
    handlers=[
        logging.FileHandler(f"{OUTPUT_DIR}/analyse.log", mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)


def main():
    logger.info(f'INPUT: {INPUT}')
    dataframe = Loader.load_analysis_from_pickle(INPUT)
    dataframe = dataframe.droplevel('TestID')
    dataframe = dataframe.droplevel('SampleRate')
    dataframe = dataframe.droplevel('WindowingFunction')
    dataframe = dataframe.droplevel('DistanceKey')
    dataframe = dataframe.droplevel('PenBrand')
    dataframe = dataframe.droplevel('PenId')
    dataframe = dataframe.droplevel('TestIteration')
    logger.info('Cleaned dataframe')
    logger.info(dataframe)

    for device in SETTING_DEVICES:
        logger.info(f'Device: {device}')
        logger.info(dataframe)
        device_dataframe = dataframe.query('Device==@device')
        grouped = device_dataframe.groupby('BufferSize')
        output_filename = f'device_{device}'

        for buffer_size, group in grouped:
            cleaned_group = group.droplevel('BufferSize')
            clicks = dataframe_index.get_clicks(dataframe)
            cleaned_group = cleaned_group.droplevel('Clicks')
            logger.info(f'Group: {buffer_size}')
            logger.info(cleaned_group)
            Output.plot_scatter(
                f"Recording {clicks} Clicks with Buffer Size {buffer_size}",
                cleaned_group.T,
                xlabel="Measurements over time",
                ylabel="Measured dB(A)",
                file_path=OUTPUT_DIR,
                file_name=f'{output_filename}-buffer_size_{buffer_size}'
            )


if __name__ == '__main__':
    main()
