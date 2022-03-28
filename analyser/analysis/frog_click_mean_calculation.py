"""

"""
import sys

import numpy as np
import pandas as pd
from scipy.signal import argrelextrema

from utils import dataframe_index, audio_calcs
from utils.data_exporter import Exporter
from utils.data_loader import Loader

import logging

from utils.output import Output

INPUT_DEVICES = '/home/michigg/GIT/uni/2021-ma-michael-goetz-data/FrogsCalibration/Test2/Converted/devices-1-aggregated-dbas.pkl'
OUTPUT_DIR = '/home/michigg/GIT/uni/2021-ma-michael-goetz-data/FrogsCalibration/Test2/Graphs/Calculations/ClickMean'

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]:\n %(message)s",
    handlers=[
        logging.FileHandler(f"{OUTPUT_DIR}/analyse-quantil.log", mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


def calc_click_mean_quantil_based(row: pd.Series, sample_rate, buffer_size, db_only=False):
    click_count = int(row.name[-2]) * 2
    logger.info('calc_click_mean')
    data: pd.Series = audio_calcs.clean_row(row=row, sample_rate=sample_rate, buffer_size=buffer_size)
    quantil = int((1 - (click_count / data.size)) * 100) / 100
    logger.info(f'Quantil: {quantil}')
    threshold = data.quantile(quantil)
    local_maxima = data.iloc[argrelextrema(data.values, np.greater)[0]]
    maxima = data.where(local_maxima > threshold, np.nan).dropna()
    db = audio_calcs.calc_average_sound_level(maxima)
    if db_only:
        return db
    return data, maxima, db


def plot_click_mean_quantil_based(row: pd.Series, sample_rate, buffer_size, output_path):
    data, maxima, db = calc_click_mean_quantil_based(row=row, sample_rate=sample_rate, buffer_size=buffer_size)

    # Plot
    logger.info(data.name)
    device = data.name[1]
    frog_size = data.name[-5]
    frog_id = int(data.name[-4])
    frog_position = data.name[-3]
    click_count = int(data.name[-2])
    distance = data.name[5]
    logger.info(
        f'Device: {device}\nFrogId: {frog_id}\nFrogSize: {frog_size}\nFrogPosition: {frog_position}\nClicks: {click_count}\nDistanceKey: {distance}')
    plot_data = data.copy().to_frame().T
    plot_data = plot_data.droplevel(0)
    plot_data = plot_data.droplevel(1)
    plot_data = plot_data.droplevel(1)
    plot_data = plot_data.droplevel(1)
    plot_data = plot_data.droplevel(1)
    plot_data = plot_data.droplevel(1)
    plot_data = plot_data.droplevel(1)
    plot_data = plot_data.droplevel(1)
    plot_data = plot_data.droplevel(1)
    plot_data = plot_data.droplevel(1)
    plot_data = plot_data.T
    Output.plot_scatter_and_maxima(
        '',
        # f"Maxima Detection Using hreshold Based On Precalculated Quantil\nClicks: {click_count}, FrogId: {frog_id}, FrogSize: {frog_size},\n FrogPosition: {frog_position}, Distance: {distance}",
        plot_data,
        maxima.to_frame(),
        xlabel="Measurements",
        ylabel="Sound Pressure Level in dB(A)",
        file_name=f'click_count_{click_count}-frog_id_{frog_id}_device_{device}-distance_{distance}',
        file_path=f'{output_path}'
    )
    return db


def plot_click_mean_global_max_based(row: pd.Series, sample_rate, buffer_size, db_range, output_path):
    data, maxima, db = audio_calcs.calc_series_click_mean(row, sample_rate, buffer_size, db_range, return_maxima=True)

    # Plot
    logger.info(data.name)
    device = data.name[1]
    frog_size = data.name[-5]
    frog_id = int(data.name[-4])
    frog_position = data.name[-3]
    click_count = int(data.name[-2])
    distance = data.name[5]
    logger.info(
        f'Device: {device}\nFrogId: {frog_id}\nFrogSize: {frog_size}\nFrogPosition: {frog_position}\nClicks: {click_count}\nDistanceKey: {distance}')
    plot_data = data.copy().to_frame().T
    plot_data = plot_data.droplevel(0)
    plot_data = plot_data.droplevel(1)
    plot_data = plot_data.droplevel(1)
    plot_data = plot_data.droplevel(1)
    plot_data = plot_data.droplevel(1)
    plot_data = plot_data.droplevel(1)
    plot_data = plot_data.droplevel(1)
    plot_data = plot_data.droplevel(1)
    plot_data = plot_data.droplevel(1)
    plot_data = plot_data.droplevel(1)
    plot_data = plot_data.T
    Output.plot_scatter_and_maxima(
        '',
        # f"Maxima Detection Using Global Max Based Threshold\nClicks: {click_count}, FrogId: {frog_id}, FrogSize: {frog_size},\n FrogPosition: {frog_position}, Distance: {distance}",
        plot_data,
        maxima.to_frame(),
        xlabel="Measurements",
        ylabel="Sound Pressure Level in dB(A)",
        file_name=f'click_count_{click_count}-frog_id_{frog_id}_device_{device}-distance_{distance}',
        file_path=f'{output_path}'
    )
    return db


def main_global_max_based(devices, sample_rate, buffer_size, db_range, output_path):
    result_path = f'{output_path}/CalcThresholdByGlobalMax/DBRange{db_range}'
    result = devices.apply(
        plot_click_mean_global_max_based,
        axis=1,
        sample_rate=sample_rate,
        buffer_size=buffer_size,
        db_range=db_range,
        output_path=result_path
    ).to_frame()
    # result = result.unstack('FrogId')
    # Exporter.save_as_csv(f'{result_path}/deviation.csv', result.std(axis=1))

    # box_plot_result = result.std(axis=1)
    # Output.box_plot(
    #     'Deviations in dB(A)',
    #     box_plot_result,
    #     file_name=f'db_range_{db_range}-boxplot',
    #     file_path=f'{result_path}'
    # )
    logger.info(result)


def main_quantil_based(devices, sample_rate, buffer_size, output_path):
    result_path = f'{output_path}/CalcThresholdByQuantil'
    result = devices.apply(
        plot_click_mean_quantil_based,
        axis=1,
        sample_rate=sample_rate,
        buffer_size=buffer_size,
        output_path=result_path
    ).to_frame()
    # result = result.unstack('FrogId')
    # Exporter.save_as_csv(f'{result_path}/deviation.csv', result.std(axis=1))

    # box_plot_result = result.std(axis=1)
    # logger.info('Plot')
    # Output.box_plot(
    #     'Deviations in dB(A)',
    #     box_plot_result.to_frame(),
    #     file_name=f'boxplot',
    #     file_path=result_path
    # )
    logger.info(result)


def main():
    devices = Loader.load_analysis_from_pickle(INPUT_DEVICES)
    device_keys = ['ONEPLUS8T', 'XPERIAZ3COM']
    devices = devices.query(
        'Device==@device_keys and DistanceKey=="MEDIUM_PERSON_ARM_MAX" and FrogSize=="SMALL" and FrogPosition=="OPEN_THUMB"')

    sample_rate = dataframe_index.get_sample_rate(devices)
    buffer_size = dataframe_index.get_buffer_size(devices)
    main_quantil_based(devices=devices, sample_rate=sample_rate, buffer_size=buffer_size, output_path=OUTPUT_DIR)
    for db_range in [10, 15, 20]:
        main_global_max_based(devices=devices, sample_rate=sample_rate, buffer_size=buffer_size, db_range=db_range,
                              output_path=OUTPUT_DIR)


if __name__ == '__main__':
    main()
