import typing
from typing import List

import numpy as np
import pandas as pd
from numpy import ndarray

from models.analysis import Analysis

import logging

from utils.a_weighting import A_weighting
from utils.audio_calcs import calc_db_from_frequency_dbs, magnitude_to_db

logger = logging.getLogger(__name__)


class Device:
    def __init__(self, title):
        self.title = title
        self.analysis_list: List[Analysis] = []

    def add_analysis(self, analysis: Analysis):
        self.analysis_list.append(analysis)

    def get_multiindex_data(self, analysis: Analysis) -> (typing.Tuple, typing.List):
        test_id = analysis.config_test.test_id
        device = analysis.config_device.device_name
        buffer_size = analysis.analysis_data.buffer_size
        sample_rate = analysis.analysis_data.sample_rate
        windowing_function = analysis.analysis_data.windowing_function

        local_index = (test_id, device, sample_rate, buffer_size, windowing_function)
        local_index_names = ['TestID', 'Device', 'SampleRate', 'BufferSize', 'WindowingFunction']

        # noise preset
        if analysis.config_noise_preset:
            local_index = local_index + (
                analysis.config_noise_preset.noise_type, analysis.config_noise_preset.noise_preset,)
            local_index_names.extend(['NoiseType', 'ConfigNoisePreset'])

        # distance info
        if analysis.config_distance:
            local_index = local_index + (analysis.config_distance.distance_key,)
            local_index_names.extend(['DistanceKey'])

        # config_frog
        if analysis.config_frog:
            local_index = local_index + (
                analysis.config_frog.frog_size, analysis.config_frog.frog_id, analysis.config_frog.frog_position,)
            local_index_names.extend(['FrogSize', 'FrogId', 'FrogPosition'])

        # config_pen
        if analysis.config_pen:
            local_index = local_index + (analysis.config_pen.pen_brand, analysis.config_pen.pen_id,)
            local_index_names.extend(['PenBrand', 'PenId'])

        # config_click
        if analysis.config_click:
            local_index = local_index + (analysis.config_click.click_count,)
            local_index_names.extend(['Clicks'])

        test_iteration = analysis.config_test.test_iteration
        local_index_names.extend(['TestIteration'])
        local_index = local_index + (test_iteration,)
        return local_index, local_index_names

    def get_dba_data_frame(self) -> pd.DataFrame:
        dataframe = pd.DataFrame()
        index = []
        index_names = []
        for analysis in self.analysis_list:
            local_index, local_index_names = self.get_multiindex_data(analysis)
            bins = range(0, len(analysis.analysis_data.dbas))

            a_series = pd.Series(analysis.analysis_data.dbas, index=bins)

            index.append(local_index)
            index_names.append(local_index_names)

            dataframe = dataframe.append(a_series, ignore_index=True)
        multi_index = pd.MultiIndex.from_tuples(index)
        multi_index.names = index_names[0]
        dataframe.set_index(multi_index, inplace=True)

        dataframe = dataframe.sort_index()
        logger.debug('get_dbas_by_noise_preset')
        logger.debug(dataframe)
        return dataframe

    def _get_rms(self, numbers: ndarray) -> ndarray:
        return np.sqrt(np.mean(numbers ** 2))

    def get_dba_data_frame_by_raw_data(self) -> pd.DataFrame:
        dataframe = pd.DataFrame()
        index = []
        index_names = []
        for analysis in self.analysis_list:
            local_index, local_index_names = self.get_multiindex_data(analysis)
            bins = range(0, len(analysis.analysis_data.amplitude_spectrums.index.values))

            amplitude_spectrums = analysis.analysis_data.amplitude_spectrums
            amplitude_spectrums = amplitude_spectrums.apply(magnitude_to_db,
                                                            axis=1,
                                                            result_type='expand')
            a_weighting = A_weighting(np.array(analysis.analysis_data.frequencies))
            amplitude_spectrums = amplitude_spectrums.add(a_weighting, axis=1)
            # Old calculation uses rms on dbs level
            # a_series: pd.Series = amplitude_spectrums.apply(self._get_rms, axis=1)
            # a_series: pd.Series = amplitude_spectrums.apply(calc_total_sound_level, axis=1)
            a_series: pd.Series = amplitude_spectrums.apply(calc_db_from_frequency_dbs, axis=1)
            a_series.index = bins
            # CHECK
            index.append(local_index)
            index_names.append(local_index_names)

            dataframe = dataframe.append(a_series, ignore_index=True)
        multi_index = pd.MultiIndex.from_tuples(index)
        multi_index.names = index_names[0]
        dataframe.set_index(multi_index, inplace=True)

        dataframe = dataframe.sort_index()
        logger.debug('get_dbas_by_noise_preset')
        logger.debug(dataframe)
        return dataframe
