import re


class ConfigNoisePreset:
    def __init__(self, noise_type, noise_types, noise_preset, noise_presets):
        self.noise_type = noise_type
        self.noise_types = noise_types
        self.noise_preset = noise_preset
        self.noise_presets = noise_presets

    @classmethod
    def from_json(cls, json_data):
        if not json_data:
            return None
        return cls(
            json_data["noiseType"],
            json_data["noiseTypes"],
            json_data["noisePreset"],
            json_data["noisePresets"]
        )

    @classmethod
    def from_json_v0(cls, json_data):
        if not json_data:
            return None
        pattern = r'(?P<test_id>.*)_(?P<test_type>\d{2})_(?P<test_iteration>\d)'
        matches = re.search(pattern, json_data["title"])
        noise_preset = 'BN'
        old_to_new_noise_preset_map = {
            "40": "40_DBA",
            "50": "50_DBA",
            "60": "60_DBA",
            "70": "70_DBA",
            "80": "80_DBA",
            "90": "90_DBA",
        }
        if matches:
            old_noise_preset = matches.group('test_type')
            noise_preset = old_to_new_noise_preset_map[old_noise_preset]
        return cls(
            'WHITE_NOISE',
            ['WHITE_NOISE'],
            noise_preset,
            ['BN', '40_DBA', '50_DBA', '60_DBA', '70_DBA', '80_DBA', '90_DBA']
        )

    def __str__(self):
        return f'Noise Preset Info: Noise Type: {self.noise_type}; Noise Preset: {self.noise_preset}'
