import logging
import sys

import pandas as pd

from utils.data_loader import Loader
from utils.output import Output

TEST_NUMBER = 2
INPUT = f'/home/michigg/GIT/uni/2021-MA-Michael-Goetz-data/data/Converted/devices-1-aggregated-dbas.pkl'


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]:\n %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)



def main():
    logger.info(f'INPUT: {INPUT}')
    dataframe = Loader.load_analysis_from_pickle(INPUT)
    dataframe = dataframe.droplevel('TestID')
    dataframe = dataframe.droplevel('SampleRate')
    dataframe = dataframe.droplevel('BufferSize')
    dataframe = dataframe.droplevel('WindowingFunction')
    dataframe = dataframe.droplevel('DistanceKey')
    dataframe = dataframe.query('TestIteration==5')
    logger.info('Cleaned dataframe')
    logger.info(dataframe)

    Output.plot_scatter(
        f"Test",
        dataframe.T,
        xlabel="Reference Noise Level",
        ylabel="Measured dB(A)"
    )

if __name__ == '__main__':
    main()
