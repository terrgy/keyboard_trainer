import json
import os

from statistics.LevelStatistics import LevelStatistics


class StatisticsManager:
    STATISTICS_FILE = './statistics.json'
    MAX_STATS_RECORDS = 10

    def __init__(self):
        self.stats = list()

        self.check_file()

        self.read_file()

    def check_file(self):
        if not os.path.isfile(self.STATISTICS_FILE):
            with open(self.STATISTICS_FILE, 'w') as f:
                f.write(json.dumps(list()))

    def read_file(self):
        file_text = ''.join(list(open(self.STATISTICS_FILE, 'r')))
        self.stats = json.loads(file_text, object_hook=LevelStatistics.from_json)

    def add_level_statistics(self, level_statistics: LevelStatistics):
        self.stats.insert(0, level_statistics)
        if len(self.stats) > self.MAX_STATS_RECORDS:
            self.stats.pop(self.MAX_STATS_RECORDS)

        self.update_file()

    def update_file(self):
        with open(self.STATISTICS_FILE, 'w') as f:
            json_lst = [stat.to_json_dict() for stat in self.stats]
            f.write(json.dumps(json_lst))
