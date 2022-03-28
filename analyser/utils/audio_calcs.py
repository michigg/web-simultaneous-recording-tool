import numpy as np
import pandas as pd
from numpy import ndarray

from utils import dataframe_index

AUDITORY_THRESHOLD = 0.00002
PAIN_THRESHOLD = 200


# TODO: documentation
def calculate_global_max(dataframe: pd.DataFrame) -> pd.DataFrame:
    return dataframe.max(axis=1).to_frame()


def ilog(dbs):
    """
    returns the inverse log of each value in the decibels array
    :param dbs: array that contains the db values
    :return: inverse log of each db value
    """
    return np.power(10, np.multiply(dbs, 0.1))


def calc_original_pressure(pressure_ratio):
    """
    calculates the original pressure value given the <code>AUDITORY_THRESHOLD</code>.
    The results are only correct if the pressure ratio is build using the <code>AUDITORY_THRESHOLD</code>.

    :param pressure_ratio: the pressure ration that shall be converted to the original value
    :return: the pressure value the ratio is based on
    """
    return pressure_ratio * (AUDITORY_THRESHOLD ** 2)


def calc_rms(pressures: ndarray) -> ndarray:
    """
    returns the root mean square of the given array

    See: https://en.wikipedia.org/wiki/Root_mean_square#Definition

    :param pressures: pressures used in the calculation
    :return: root mean square
    """
    return np.sqrt(np.mean(pressures ** 2))


def calc_sound_pressure_level(p_rms):
    """
    Calculates the sound pressure level of the given <code>p_rms</code> based on the <code>AUDITORY_THRESHOLD</code>.
    If it is a ratio please use the <code>calc_sound_pressure_level_using_ratio</code> method.

    :param p_rms: the pressure value that should be converted to decibel
    :return: the pressure value
    """
    spl = 10 * np.log10(p_rms / AUDITORY_THRESHOLD ** 2)
    return np.round(spl, decimals=4)


def calc_sound_pressure_level_using_ratio(p_ratio):
    """
    Calculates the sound pressure level of the given <code>p_ratio</code>.
    If it is not a ratio please use the <code>calc_sound_pressure_level</code> method.

    :param p_ratio: the pressure ratio value that should be converted to decibel
    :return: the pressure value
    """
    spl = 10 * np.log10(p_ratio)
    return np.round(spl, decimals=4)


def calc_db_from_frequency_dbs(dbs: pd.Series):
    """
    Calculates a single decibel value given multiple decibels from the frequency domain

    :param dbs: array of db values
    :return: db value that is derived from the dbs param
    """
    if not dbs.any():
        return np.nan
    pressures = calc_original_pressure(ilog(dbs))
    p_rms = calc_rms(pressures)
    return calc_sound_pressure_level(p_rms)


def calc_total_sound_level(dbs: pd.Series):
    """
    Calculates the total sound level of a given series of dbs measured over time
    :param dbs: series of measured dbs
    :return: total sound level of that db
    """
    if not dbs.any():
        return np.nan
    pressures_ration_sum = np.sum(ilog(dbs))
    return calc_sound_pressure_level_using_ratio(pressures_ration_sum)


def calc_average_sound_level(dbs: pd.Series):
    if not dbs.any():
        return np.nan
    #     See https://www.schweizer-fn.de/akustik/schallpegelaenderung/schallpegel.php#gesamtschallpegel
    mean = np.divide(np.sum(ilog(dbs)), len(dbs))
    return calc_sound_pressure_level_using_ratio(mean)


def get_frequencies(sample_rate: int, buffer_size: int):
    return [get_frequency(i, sample_rate, buffer_size) for i in range(0, int(buffer_size / 2))]


def get_frequency_resolution(sample_rate: int, buffer_size: int) -> float:
    return np.true_divide(sample_rate, buffer_size)


def get_frequency(bin_index: 0, sample_rate: int, buffer_size: int) -> float:
    return np.round(np.multiply(bin_index, get_frequency_resolution(sample_rate, buffer_size)), decimals=4)


def get_milliseconds_per_bin(sample_rate: int, buffer_size: int) -> int:
    return np.round(np.multiply(np.divide(buffer_size, sample_rate), 1000), decimals=0)


def get_bin_count_by_millisecond(x: int, sample_rate: int, buffer_size: int) -> float:
    milliseconds_per_bin = get_milliseconds_per_bin(sample_rate, buffer_size)
    return np.divide(x, milliseconds_per_bin)


def get_index_of_bin_at_x_milliseconds_from_first(milliseconds: int, sample_rate: int, buffer_size: int) -> int:
    return int(np.ceil(get_bin_count_by_millisecond(milliseconds, sample_rate, buffer_size)))


def get_index_of_bin_at_x_milliseconds_from_last(milliseconds: int, sample_rate: int, buffer_size: int) -> int:
    return int(np.trunc(get_bin_count_by_millisecond(milliseconds, sample_rate, buffer_size)))


def clean_row(row: pd.Series, sample_rate, buffer_size):
    start_bin = get_index_of_bin_at_x_milliseconds_from_last(1000, sample_rate, buffer_size)
    return row.loc[start_bin:]


def calc_series_click_mean(row: pd.Series, sample_rate, buffer_size, db_range=10, return_maxima=False):
    data = clean_row(row=row, sample_rate=sample_rate, buffer_size=buffer_size)
    row.dropna()
    max_click = data.max()
    maxima = data.where(data > max_click - db_range, np.nan).dropna()
    db = calc_average_sound_level(maxima)
    if return_maxima:
        return data, maxima, db
    return db


def calc_dataframe_click_mean(dataframe: pd.DataFrame, db_range=10):
    sample_rate = dataframe_index.get_sample_rate(dataframe)
    buffer_size = dataframe_index.get_buffer_size(dataframe)
    result = dataframe.apply(
        calc_series_click_mean,
        axis=1,
        sample_rate=sample_rate,
        buffer_size=buffer_size,
        db_range=db_range
    ).to_frame()
    return result


def magnitude_to_db(magnitude):
    magnitude = np.asarray(magnitude)
    if not magnitude.any():
        result = np.empty(magnitude.shape)
        result[:] = np.nan
        return result
    # powered_ref = AUDITORY_THRESHOLD ** 2
    # powered_magnitude = magnitude ** 2
    db = 20.0 * np.log10(magnitude / AUDITORY_THRESHOLD)
    # db = np.where(db < 0, 0, db)
    return db