class ConfigClick:
    def __init__(self, click_count):
        self.click_count = click_count

    @classmethod
    def from_json(cls, json_data):
        if not json_data:
            return None
        return cls(
            json_data["clickCount"],
        )

    def __str__(self):
        return f'Click Count: {self.click_count}'
