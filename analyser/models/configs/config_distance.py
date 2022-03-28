class ConfigDistance:
    def __init__(self, distance_key, distance_keys):
        self.distance_key = distance_key
        self.distance_keys = distance_keys

    @classmethod
    def from_json_v0(cls, json_data):
        if not json_data:
            return None
        return cls(
            "50m",
            ["50m"]
        )

    @classmethod
    def from_json_v01(cls, json_data):
        if not json_data:
            return None
        return cls(
            json_data["distanceKey"],
            ["0m",
             "SMALL_MEDIUM_PERSON_SHOULDER_MAX",
             "MEDIUM_PERSON_SHOULDER_MAX",
             "SMALL_PERSON_ARM_MAX",
             "MEDIUM_PERSON_ARM_MAX"
             ]
        )

    @classmethod
    def from_json(cls, json_data):
        if not json_data:
            return None
        return cls(
            json_data["distanceKey"],
            json_data["distanceKeys"]
        )

    def __str__(self):
        return f'Distance: {self.distance_key}'
