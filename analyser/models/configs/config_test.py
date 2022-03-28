import re


class ConfigTest:
    def __init__(self, test_id, description, test_iteration):
        self.test_id = test_id
        self.description = description
        self.test_iteration = test_iteration

    @classmethod
    def from_json(cls, json_data):
        if not json_data:
            return None
        return cls(
            json_data["testId"],
            json_data["description"],
            json_data["testIteration"]
        )

    @classmethod
    def from_json_v0(cls, json_data):
        if not json_data:
            return None
        pattern = r'(?P<test_id>.*)_(?P<test_type>\d{2})_(?P<test_iteration>\d)'
        matches = re.search(pattern, json_data["title"])
        if not matches:
            pattern = r'(?P<test_id>.*)(?P<test_iteration>\d)'
            matches = re.search(pattern, json_data["title"])
        test_id = matches.group('test_id')
        if test_id == 'GROUND' or test_id == 'H':
            test_id = 'GROUND_TRUTH'
        test_iteration = matches.group('test_iteration')
        return cls(
            test_id,
            '',
            test_iteration
        )
    @classmethod
    def from_json_v01(cls, json_data):
        if not json_data:
            return None
        return cls(
            json_data["testId"],
            '',
            json_data["testNumber"],
        )

    def __str__(self):
        return f'Test Info: Test Id: {self.test_id}; Test Iteration: {self.test_iteration}'