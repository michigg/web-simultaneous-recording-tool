import pandas as pd


def prepare_dataframe(dataframe: pd.DataFrame):
    prepared_dataframe = dataframe.droplevel('TestID')
    prepared_dataframe = prepared_dataframe.droplevel('SampleRate')
    prepared_dataframe = prepared_dataframe.droplevel('BufferSize')
    prepared_dataframe = prepared_dataframe.droplevel('WindowingFunction')
    prepared_dataframe = prepared_dataframe.droplevel('NoiseType')
    prepared_dataframe = prepared_dataframe.droplevel('DistanceKey')
    prepared_dataframe = prepared_dataframe.unstack('ConfigNoisePreset')
    prepared_dataframe = prepared_dataframe.drop('BN', axis=1, level=1)
    prepared_dataframe = prepared_dataframe.droplevel(level=0, axis=1)
    return prepared_dataframe


def get_deviation_to_reference_per_device(devices_dataframe: pd.DataFrame,
                                          reference_dataframe: pd.DataFrame) -> pd.DataFrame:
    return devices_dataframe.subtract(reference_dataframe.T['REFERENCE'], axis=1)
