import json


class MistakesHeatmap:
    def __init__(self):
        self.hits = {}

    def add_mistake(self, char):
        char = char.lower()
        self.hits.setdefault(char, 0)
        self.hits[char] += 1

    def make_list(self):
        result = list()

        self.hits = dict(reversed(sorted(self.hits.items(), key=lambda item: item[1])))
        for key, value in self.hits.items():
            if key == ' ':
                key = 'Space'
            result.append("{}: {} times".format(key, value))
        return result

    def to_json_dict(self):
        dct = {
            'hits': self.hits,
            '__class__': 'MistakesHeatmap'
        }
        return dct

    @staticmethod
    def from_json(json_dict):
        if json_dict.get('__class__', None) != 'MistakesHeatmap':
            return json_dict

        json_dict.pop('__class__')
        res = MistakesHeatmap()
        res.__dict__.update(json_dict)
        return res
