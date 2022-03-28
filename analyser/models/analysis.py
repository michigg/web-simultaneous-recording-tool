import logging

from models.analysis_data import AnalysisData
from models.configs.config_click import ConfigClick
from models.configs.config_device import ConfigDevice
from models.configs.config_distance import ConfigDistance
from models.configs.config_frog import ConfigFrog
from models.configs.config_noise_preset import ConfigNoisePreset
from models.configs.config_pen import ConfigPen
from models.configs.config_test import ConfigTest

logger = logging.getLogger(__name__)


class Analysis:
    def __init__(
            self,
            path,
            device,
            test,
            noise_preset,
            distance_info,
            frog_info,
            pen_info,
            click_info,
            analysis
    ):
        self.path = path
        self.config_device: ConfigDevice = device
        self.config_test: ConfigTest = test
        self.config_noise_preset: ConfigNoisePreset = noise_preset
        self.config_distance: ConfigDistance = distance_info
        self.config_frog: ConfigFrog = frog_info
        self.config_pen: ConfigPen = pen_info
        self.config_click: ConfigClick = click_info
        self.analysis_data: AnalysisData = analysis

    @classmethod
    def from_json(cls, json_data, path: str):
        if 'audio' not in json_data and 'config' not in json_data:
            logger.info('Version 0.0 data format found')
            return cls(
                path,
                ConfigDevice.from_json_v0(json_data),
                ConfigTest.from_json_v0(json_data),
                ConfigNoisePreset.from_json_v0(json_data),
                ConfigDistance.from_json_v0(json_data),
                None,
                None,
                None,
                AnalysisData.from_json_v0(json_data)
            )

        if 'audio' not in json_data and 'config' in json_data:
            logger.info('Version 0.1 data format found')
            return cls(
                path,
                ConfigDevice.from_json_v0(json_data["config"]),
                ConfigTest.from_json_v01(json_data["config"]),
                None,
                ConfigDistance.from_json_v01(json_data["config"]),
                ConfigFrog.from_json_v01(json_data["config"]),
                None,
                None,
                AnalysisData.from_json_v01(json_data)
            )
        logger.info('Version 1.0 data format found')
        return cls(
            path,
            ConfigDevice.from_json(json_data["local"]) if 'local' in json_data else None,
            ConfigTest.from_json(json_data["base"]) if 'base' in json_data else None,
            ConfigNoisePreset.from_json(json_data["noisePreset"]) if 'noisePreset' in json_data else None,
            ConfigDistance.from_json(json_data["distance"]) if 'distance' in json_data else None,
            ConfigFrog.from_json(json_data["frog"]) if 'frog' in json_data else None,
            ConfigPen.from_json(json_data["pen"]) if 'pen' in json_data else None,
            ConfigClick.from_json(json_data["clickCount"]) if 'clickCount' in json_data else None,
            AnalysisData.from_json(json_data["audio"]) if 'audio' in json_data else None
        )
