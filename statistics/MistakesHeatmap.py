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
