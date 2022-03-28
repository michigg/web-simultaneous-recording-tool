import numpy as np
import pandas as pd

from utils.audio_calcs import get_frequencies

LOWEST_AUDIBLE_FREQUENCY = 20
HIGHEST_AUDIBLE_FREQUENCY = 20000  # 70000


class AnalysisData:
    LOWEST_AUDIBLE_FREQUENCY = LOWEST_AUDIBLE_FREQUENCY
    HIGHEST_AUDIBLE_FREQUENCY = HIGHEST_AUDIBLE_FREQUENCY

    def __init__(
            self,
            duration_seconds,
            sample_rate,
            buffer_size,
            number_of_input_channels,
            windowing_function,
            lowest_perceptible_frequency,
            highest_perceptible_frequency,
            frequencies,
            start_timestamp,
            stop_timestamp,
            timestamps,
            amplitude_spectrums,
            # dbs,
            dbas,

    ):
        self.duration_seconds = duration_seconds
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
        self.number_of_input_channels = number_of_input_channels
        self.windowing_function = windowing_function
        self.lowest_perceptible_frequency = lowest_perceptible_frequency
        self.highest_perceptible_frequency = highest_perceptible_frequency
        self.frequencies = frequencies
        self.start_timestamp = start_timestamp
        self.stop_timestamp = stop_timestamp
        self.timestamps = timestamps
        self.amplitude_spectrums = amplitude_spectrums
        # self.dbs = dbs
        self.dbas = dbas

        self.amplitude_spectrums: pd.DataFrame = pd.DataFrame(
            amplitude_spectrums,
            index=self.timestamps,
            columns=self.get_frequencies() if self.get_frequencies() else range(0, int(self.buffer_size / 2))
        )
        self.lowest_bin = self.get_lowest_audible_bin()
        self.highest_bin = self.get_highest_audible_bin()
        self.frequencies = self.frequencies[self.lowest_bin: self.highest_bin]
        self.amplitude_spectrums: pd.DataFrame = self.amplitude_spectrums.iloc[:,
                                                 range(self.lowest_bin, self.highest_bin)]

    @classmethod
    def from_json(cls, json_data):
        if not json_data:
            return None
        return cls(
            json_data["durationSeconds"],
            json_data["sampleRate"],
            json_data["bufferSize"],
            json_data["numberOfInputChannels"],
            json_data["windowingFunction"],
            json_data["lowestPerceptibleFrequency"],
            json_data["highestPerceptibleFrequency"],
            json_data["frequencies"],
            json_data["startTimestamp"],
            json_data["stopTimestamp"],
            json_data["timestamps"],
            json_data["amplitudeSpectrums"],
            # json_data["dbs"],
            json_data["dbas"],
        )

    @classmethod
    def from_json_v0(cls, json_data):
        if not json_data:
            return None
        duration_seconds = np.round((json_data["stopTimestamp"] - json_data["startTimestamp"]) / 1000)
        frequencies = get_frequencies(json_data["sampleRate"], json_data["blockSize"])
        return cls(
            duration_seconds,
            json_data["sampleRate"],
            json_data["blockSize"],
            None,
            'hanning',
            -1,
            -1,
            frequencies,
            json_data["startTimestamp"],
            json_data["stopTimestamp"],
            json_data["timestamps"],
            json_data["amplitudeSpectrums"],
            []
        )
    @classmethod
    def from_json_v01(cls, json_data):
        if not json_data:
            return None
        frequencies = get_frequencies(json_data["sampleRate"], json_data["blockSize"])
        return cls(
            json_data["config"]["durationSeconds"],
            json_data["config"]["sampleRate"],
            json_data["config"]["bufferSize"],
            None,
            'hanning',
            -1,
            -1,
            frequencies,
            json_data["startTimestamp"],
            json_data["stopTimestamp"],
            json_data["timestamps"],
            json_data["amplitudeSpectrums"],
            []
        )

    def get_amplitude_spectrums(self, start_timestamp=1000):
        index = self._find_index(start_timestamp)
        return self.amplitude_spectrums.iloc[index:]

    def get_timestamps_at_timestamp(self, start_timestamp=1000):
        index = self._find_index(start_timestamp)
        return self.amplitude_spectrums[index:]

    def _find_index(self, value) -> int:
        for index, element in enumerate(self.timestamps):
            if element >= value:
                return index

    def get_duration(self):
        return self.stop_timestamp - self.start_timestamp

    def get_frequencies(self):
        return self.frequencies

    def get_frequency_resolution(self):
        return np.true_divide(self.sample_rate, self.buffer_size)

    def get_frequency(self, bin_index: 0):
        return np.multiply(bin_index, self.get_frequency_resolution())

    def get_lowest_audible_bin(self):
        min_bin = np.trunc(np.divide(self.LOWEST_AUDIBLE_FREQUENCY, self.get_frequency_resolution())) + 1
        return int(min_bin)

    def get_highest_audible_bin(self):
        max_bin = np.trunc(np.divide(self.HIGHEST_AUDIBLE_FREQUENCY, self.get_frequency_resolution()))
        return int(max_bin)

    def __str__(self):
        return f'Analysis Info: Duration: {self.duration_seconds}; Bins: {len(self.timestamps)}; Sample Rate: {self.sample_rate}; Buffer Size: {self.buffer_size}'
