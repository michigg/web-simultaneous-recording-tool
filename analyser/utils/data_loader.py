import glob
import json
import pandas as pd

from models.analysis import Analysis
from models.devices import Devices

import logging

logger = logging.getLogger(__name__)


class Loader:
    @staticmethod
    def load_analysis_from_csv(path: str, index_col=0, header=0) -> pd.DataFrame:
        return pd.read_csv(path, sep=';', header=header, index_col=index_col)

    @staticmethod
    def load_analysis_from_json(directory: str) -> Devices:
        file_paths = glob.glob(f'{directory}/**/*.json', recursive=True)
        devices = Devices()
        logger.info(f'load_analysis: Found {len(file_paths)} files.')
        for path in file_paths:
            logger.info(f'load_analysis: load: {path}')
            with open(path) as file:
                devices.add_analysis(Analysis.from_json(json.load(file), path))
        devices.print_all()
        return devices

    @staticmethod
    def load_analysis_from_pickle(path: str) -> pd.DataFrame:
        logger.info(f'load_analysis_from_pickle: path: {path}')
        dataframe = pd.read_pickle(path)
        logger.info('load_analysis_from_pickle: loaded dataframe')
        logger.info(dataframe)
        return pd.read_pickle(path)
