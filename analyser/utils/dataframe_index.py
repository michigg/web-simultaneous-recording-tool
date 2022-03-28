import pandas as pd


def get_device(dataframe: pd.DataFrame) -> str:
    device = dataframe.index.get_level_values('Device').unique()
    if len(device) != 1:
        raise Exception(f'Different devices found: {device}')
    return device[0]


def get_buffer_size(dataframe: pd.DataFrame) -> int:
    buffer_size = dataframe.index.get_level_values('BufferSize').unique()
    if len(buffer_size) != 1:
        raise Exception(f'Different buffer sizes found: {buffer_size}')
    return int(buffer_size[0])


def get_sample_rate(dataframe: pd.DataFrame) -> int:
    sample_rate = dataframe.index.get_level_values('SampleRate').unique()
    if len(sample_rate) != 1:
        print(dataframe)
        raise Exception(f'Different sample rates found: {sample_rate}')
    return int(sample_rate[0])


def get_clicks(dataframe: pd.DataFrame) -> int:
    clicks = dataframe.index.get_level_values('Clicks').unique()
    if len(clicks) != 1:
        raise Exception(f'Different click counts found: {clicks}')
    return int(clicks[0])


def get_pen_brand(dataframe: pd.DataFrame) -> str:
    pen_brand = dataframe.index.get_level_values('PenBrand').unique()
    if len(pen_brand) != 1:
        raise Exception(f'Different pen brands found: {pen_brand}')
    return pen_brand[0]


def get_pen_id(dataframe: pd.DataFrame) -> int:
    pen_id = dataframe.index.get_level_values('PenId').unique()
    if len(pen_id) != 1:
        raise Exception(f'Different Pen Ids found: {pen_id}')
    return int(pen_id[0])


def get_frog_id(dataframe: pd.DataFrame) -> int:
    print(dataframe)
    frog_id = dataframe.index.get_level_values('FrogId').unique()
    if len(frog_id) != 1:
        raise Exception(f'Different FrogId Ids found: {frog_id}')
    return int(frog_id[0])


def get_frog_position(dataframe: pd.DataFrame) -> int:
    frog_position = dataframe.index.get_level_values('FrogPosition').unique()
    if len(frog_position) != 1:
        raise Exception(f'Different Frog Positions found: {frog_position}')
    return int(frog_position[0])


def get_frog_size(dataframe: pd.DataFrame) -> int:
    frog_size = dataframe.index.get_level_values('FrogSize').unique()
    if len(frog_size) != 1:
        raise Exception(f'Different Frog Sizes found: {frog_size}')
    return int(frog_size[0])


def get_test_iteration(dataframe: pd.DataFrame) -> int:
    test_iteration = dataframe.index.get_level_values('TestIteration').unique()
    if len(test_iteration) != 1:
        raise Exception(f'Different test iteration found: {test_iteration}')
    return int(test_iteration[0])
