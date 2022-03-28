class ConfigDevice:
    def __init__(self, device_name, input_device_info):
        self.device_name = device_name
        self.input_device_info = input_device_info

    @classmethod
    def from_json(cls, json_data):
        if not json_data:
            return None
        return cls(
            json_data["deviceName"],
            json_data["inputDeviceInfo"]
        )

    @classmethod
    def from_json_v0(cls, json_data):
        if not json_data:
            return None
        device_name = json_data["deviceName"]
        if device_name == 'TAB':
            device_name = 'LENOVOTAB'
        return cls(
            device_name,
            ''
        )

    def __str__(self):
        input_device_info_label = self.input_device_info["label"] if "label" in self.input_device_info else ''
        return f'Device Name: {self.device_name}; Input Device Label: {input_device_info_label}'
