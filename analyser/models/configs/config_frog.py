class ConfigFrog:
    def __init__(self, frog_id, frog_size, frog_sizes, frog_position, frog_positions):
        self.frog_id = frog_id
        self.frog_size = frog_size
        self.frog_sizes = frog_sizes
        self.frog_position = frog_position
        self.frog_positions = frog_positions

    @classmethod
    def from_json_v01(cls, json_data):
        if not json_data:
            return None
        print(json_data)
        return cls(
            json_data["frogId"],
            json_data["frogSize"],
            None,
            json_data["frogPosition"],
            None
        )

    @classmethod
    def from_json(cls, json_data):
        if not json_data:
            return None
        return cls(
            json_data["frogId"],
            json_data["frogSize"],
            json_data["frogSizes"],
            json_data["frogPosition"],
            json_data["frogPositions"]
        )

    def __str__(self):
        return f'Size: {self.frog_size}; ID: {self.frog_id}'
