import pandas as pd
import logging

logger = logging.getLogger(__name__)


class Exporter:
    @staticmethod
    def save_as_pickle(path: str, dataframe: pd.DataFrame):
        logger.info(f'save dataframe as pickle using: {path}')
        logger.info('Dataframe to save')
        logger.info(dataframe)
        dataframe.to_pickle(path)

    @staticmethod
    def save_as_csv(path: str, dataframe: pd.DataFrame):
        logger.info(f'save dataframe as csv using: {path}')
        logger.info('Dataframe to save')
        # logger.info(dataframe)
        dataframe.to_csv(path, sep=';')
