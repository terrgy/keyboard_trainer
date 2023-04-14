from statistics.MistakesHeatmap import MistakesHeatmap
import tkinter as ttk
import json


class LevelStatistics:
    stats_names = ['chars_count', 'mistakes', 'mistakes_percentage', 'elapsed_time', 'average_speed']
    SECONDS_IN_MINUTE = 60

    def __init__(self):
        self.text_len, self.mistakes = 0, 0
        self.mistakes_heatmap = MistakesHeatmap()
        self.elapsed_time = 0

        self.is_finished = False
        self.level_name = ''

        self.stats_str_vars = dict()

    def create_str_vars(self):
        for stat in self.stats_names:
            self.stats_str_vars[stat] = ttk.StringVar()
        self.update_str_vars()

    def update_str_vars(self):
        self.stats_str_vars['chars_count'].set('Symbols:\n{}'.format(self.text_len))
        self.stats_str_vars['mistakes'].set('Mistakes:\n{}'.format(self.mistakes))
        self.stats_str_vars['mistakes_percentage'].set('Percentage:\n{:.2%}'.
                                                       format(self.get_mistakes_percentage()))
        self.stats_str_vars['elapsed_time'].set('Time:\n{:.1f}'.format(self.elapsed_time))
        self.stats_str_vars['average_speed'].set(
            'Average speed:\n{:.1f} symb/min'.format(self.get_average_speed()))

    def get_mistakes_percentage(self):
        if not self.text_len:
            return 0
        return self.mistakes / self.text_len

    def get_average_speed(self):
        if not self.elapsed_time:
            return 0
        return self.text_len * self.SECONDS_IN_MINUTE / self.elapsed_time

    def add_correct(self, char):
        self.text_len += 1

    def add_mistake(self, char):
        self.text_len += 1
        self.mistakes += 1
        self.mistakes_heatmap.add_mistake(char)

    def to_json_dict(self):
        dct = {
            'text_len': self.text_len,
            'mistakes': self.mistakes,
            'mistakes_heatmap': self.mistakes_heatmap.to_json_dict(),
            'elapsed_time': self.elapsed_time,
            'is_finished': self.is_finished,
            'level_name': self.level_name,
            '__class__': 'LevelStatistics',
        }
        return dct

    @staticmethod
    def from_json(json_dict):
        if json_dict.get('__class__', None) != 'LevelStatistics':
            return json_dict

        res = LevelStatistics()
        heatmap = json_dict.pop('mistakes_heatmap')
        json_dict.pop('__class__')
        res.__dict__.update(json_dict)
        res.mistakes_heatmap = MistakesHeatmap.from_json(heatmap)
        return res
