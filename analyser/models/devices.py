import pandas as pd

from models.analysis import Analysis
from models.device import Device

import logging

logger = logging.getLogger(__name__)


class Devices:
    def __init__(self):
        self.devices: dict[str, Device] = {}

    def add_analysis(self, analysis: Analysis):
        if analysis.config_device.device_name not in self.devices:
            self.devices[analysis.config_device.device_name] = Device(analysis.config_device.device_name)
        self.devices[analysis.config_device.device_name].add_analysis(analysis)

    def get_dba_data_frame(self) -> pd.DataFrame:
        dataframes = []
        for device_key in self.devices:
            dataframes.append(self.devices[device_key].get_dba_data_frame())
        return pd.concat(dataframes)

    def get_dba_data_frame_by_raw_data(self) -> pd.DataFrame:
        dataframes = []
        for device_key in self.devices:
            dataframes.append(self.devices[device_key].get_dba_data_frame_by_raw_data())
        return pd.concat(dataframes)

    def print_all(self):
        result = f'Devices {len(self.devices)}\n'
        for device_key in self.devices:
            device = self.devices[device_key]
            result += f'{device.title} - Analysis List: {len(device.analysis_list)}\n'

            for analysis in device.analysis_list:
                result += f'\t{analysis}\n'
                for attribute, value in analysis.__dict__.items():
                    result += f'\t\t{attribute:<15} = {value}\n'
            result += '\n'
        logger.info(result)

    def __str__(self):
        result = f'Devices {len(self.devices)}\n'
        for device_key in self.devices:
            device = self.devices[device_key]
            result += f'{device.title} - AnalysisList: {len(device.analysis_list)}\n'
            result += '\n'
        return result
