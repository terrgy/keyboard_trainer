import os

from levels_manager.Level import Level


class LevelsManager:
    LEVELS_DIR = './levels_manager/levels/'

    def __init__(self):
        self.levels = dict()

        self.read_levels()

    def read_levels(self):
        with os.scandir(self.LEVELS_DIR) as files:
            for file in files:
                if os.path.isfile(file.path) and file.name.endswith('.level'):
                    level = Level.read_from_file(file.path)
                    self.levels[level.name] = level

    def levels_count(self):
        return len(self.levels)

    def get_level(self, name):
        return self.levels[name]

    def get_levels_list(self):
        return self.levels.keys()
