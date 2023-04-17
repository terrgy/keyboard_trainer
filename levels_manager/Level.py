import json


class Level:
    def __init__(self):
        self.name = ''
        self.text = ''

    @staticmethod
    def read_from_file(filename):
        with open(filename, 'r') as f:
            file_text = ''.join(list(f))
        json_object = json.loads(file_text)
        level = Level()
        level.name = json_object['name']
        level.text = json_object['text']
        return level
