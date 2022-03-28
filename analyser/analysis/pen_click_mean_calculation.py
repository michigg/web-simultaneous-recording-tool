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

# INPUT_DEVICES = '/home/michigg/GIT/uni/2021-ma-michael-goetz-data/PensCalibration/Test2/Converted/devices-1-aggregated-dbas-distance_0m-device.pkl'
INPUT_DEVICES = '/home/michigg/GIT/uni/2021-ma-michael-goetz-data/PensCalibration/Test2/Converted/devices-1-aggregated-dbas.pkl'
OUTPUT_DIR = '/home/michigg/GIT/uni/2021-ma-michael-goetz-data/PensCalibration/Test2/Graphs/ClickMean'

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


def save_short_dataframe():
    output_path = '/home/michigg/GIT/uni/2021-ma-michael-goetz-data/PensCalibration/Test2/Converted/devices-1-aggregated-dbas.pkl'
    devices = Loader.load_analysis_from_pickle(INPUT_DEVICES)
    dataframe = devices.query('DistanceKey=="MEDIUM_PERSON_ARM_MAX" and Device=="XPERIAZ3COM2"')
    logger.info('Prepared Dataframe')
    logger.info(dataframe)
    Exporter.save_as_pickle(
        '/home/michigg/GIT/uni/2021-ma-michael-goetz-data/PensCalibration/Test2/Converted/devices-1-aggregated-dbas-distance_0m-device.pkl',
        dataframe)
    Exporter.save_as_csv(
        '/home/michigg/GIT/uni/2021-ma-michael-goetz-data/PensCalibration/Test2/Converted/devices-1-aggregated-dbas-distance_0m-device.csv',
        dataframe)


def calc_click_mean(row: pd.Series, sample_rate, buffer_size):
    click_count = int(row.name[-2])
    logger.info('calc_click_mean')
    data = audio_calcs.clean_row(row=row, sample_rate=sample_rate, buffer_size=buffer_size)
    quantil = int((1 - (click_count / data.size)) * 100) / 100
    logger.info(f'Quantil: {quantil}')
    threshold = data.quantile(quantil)
    maxima = data.where(data > threshold, np.nan).dropna()
    db = maxima.mean()
    return data, maxima, db


def plot_click_mean(row: pd.Series, sample_rate, buffer_size):
    data, maxima, db = calc_click_mean(row, sample_rate, buffer_size)

    # Plot
    logger.info(data.name)
    device = data.name[1]
    pen_id = int(data.name[-3])
    click_count = int(data.name[-2])
    distance = data.name[5]
    logger.info(f'Device: {device}')
    logger.info(f'PenId: {pen_id}')
    logger.info(f'Clicks: {click_count}')
    logger.info(f'DistanceKey: {distance}')
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
    plot_data = plot_data.T
    Output.plot_scatter_and_maxima(
        f"Maxima Detection Using hreshold Based On Precalculated Quantil\nClicks: {click_count}, PenId: {pen_id}, Distance: {distance}",
        plot_data,
        maxima.to_frame(),
        xlabel="Measurements",
        ylabel="Sound Pressure Level in dB(A)",
        file_name=f'click_count_{click_count}-pen_id_{pen_id}_device_{device}-distance_{distance}',
        file_path=f'{OUTPUT_DIR}/CalcThresholdByQuantil'
    )
    return maxima.mean()


def calc_click_mean_alt(row: pd.Series, sample_rate, buffer_size, db_range):
    logger.info('calc_click_mean_alt')
    data = audio_calcs.clean_row(row=row, sample_rate=sample_rate, buffer_size=buffer_size)
    row.dropna()
    logger.info(data)
    logger.info(data.name)
    logger.info(data.index)
    max_click = data.max()
    maxima = data.where(data > max_click - db_range, np.nan).dropna()
    db = maxima.mean()
    return data, maxima, db


def plot_click_mean_alt(row: pd.Series, sample_rate, buffer_size, db_range):
    data, maxima, db = calc_click_mean_alt(row, sample_rate, buffer_size, db_range)

    # Plot
    logger.info(data.name)
    device = data.name[1]
    pen_id = int(data.name[-3])
    click_count = int(data.name[-2])
    distance = data.name[5]
    logger.info(f'Device: {device}')
    logger.info(f'PenId: {pen_id}')
    logger.info(f'Clicks: {click_count}')
    logger.info(f'DistanceKey: {distance}')
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
    plot_data = plot_data.T
    Output.plot_scatter_and_maxima(
        f"Maxima Detection Using Global Max Based Threshold\nClicks: {click_count}, PenId: {pen_id}, Distance: {distance}",
        plot_data,
        maxima.to_frame(),
        xlabel="Measurements",
        ylabel="Sound Pressure Level in dB(A)",
        file_name=f'db_range_{db_range}-click_count_{click_count}-pen_id_{pen_id}_device_{device}-distance_{distance}',
        file_path=f'{OUTPUT_DIR}/CalcThresholdByGlobalMax'
    )
    return db


def main():
    devices = Loader.load_analysis_from_pickle(INPUT_DEVICES)
    # result = devices.apply(calc_click_mean, axis=1)
    device_keys = ['ONEPLUS8T', 'XPERIAZ3COM']
    devices = devices.query('Device==@device_keys and DistanceKey=="MEDIUM_PERSON_ARM_MAX"')
    sample_rate = dataframe_index.get_sample_rate(devices)
    buffer_size = dataframe_index.get_buffer_size(devices)
    db_range = 15
    result = devices.apply(plot_click_mean_alt, axis=1, sample_rate=sample_rate, buffer_size=buffer_size,
                           db_range=db_range).to_frame()
    result = result.unstack('PenId')
    Exporter.save_as_csv(f'{OUTPUT_DIR}/CalcThresholdByGlobalMax/db_range_{db_range}.csv', result)
    Exporter.save_as_csv(f'{OUTPUT_DIR}/CalcThresholdByGlobalMax/db_range_{db_range}_deviation.csv', result.std(axis=1))

    box_plot_result = result.std(axis=1)
    Output.box_plot(
        'Deviations in dB(A)',
        box_plot_result,
        file_name=f'db_range_{db_range}-boxplot',
        file_path=f'{OUTPUT_DIR}/CalcThresholdByGlobalMax'
    )
    logger.info(result)


def main_quantil_based():
    devices = Loader.load_analysis_from_pickle(INPUT_DEVICES)
    device_keys = ['ONEPLUS8T', 'XPERIAZ3COM']
    devices = devices.query('Device==@device_keys and DistanceKey=="MEDIUM_PERSON_ARM_MAX"')
    sample_rate = dataframe_index.get_sample_rate(devices)
    buffer_size = dataframe_index.get_buffer_size(devices)
    db_range = 15
    result = devices.apply(plot_click_mean, axis=1, sample_rate=sample_rate, buffer_size=buffer_size).to_frame()
    result = result.unstack('PenId')
    Exporter.save_as_csv(f'{OUTPUT_DIR}/CalcThresholdByQuantil/db_range_{db_range}.csv', result)
    Exporter.save_as_csv(f'{OUTPUT_DIR}/CalcThresholdByQuantil/db_range_{db_range}_deviation.csv', result.std(axis=1))

    box_plot_result = result.std(axis=1)
    Output.box_plot(
        'Deviations in dB(A)',
        box_plot_result,
        file_name=f'db_range_{db_range}-boxplot',
        file_path=f'{OUTPUT_DIR}/CalcThresholdByQuantil'
    )
    logger.info(result)


if __name__ == '__main__':
    # main()
    main_quantil_based()
