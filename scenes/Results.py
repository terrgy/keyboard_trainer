from Object import Object
from scenes.BaseScene import BaseScene
import tkinter as ttk

from statistics.LevelStatistics import LevelStatistics


class ResultsScene(BaseScene):
    font = ("Arial", 20)

    def __init__(self, app):
        super().__init__(app)
        self.level_statistics = LevelStatistics()

        for c in range(2):
            self.app.columnconfigure(index=c, weight=1)

        self.stats = dict()
        self.create_stats()

        self.heatmap_text = ttk.StringVar()
        self.objects.append(Object(
            ttk.Label(textvariable=self.heatmap_text, font=self.font),
            grid={'row': 0, 'column': 1}
        ))

    def create_stats(self):
        index = 0
        for stat in self.level_statistics.stats_names:
            self.stats[stat] = Object(
                ttk.Label(font=self.font),
                grid={"row": index, "column": 0},
            )
            index += 1

        self.objects.extend(self.stats.values())

    def on_activate(self, level_statistics: LevelStatistics):
        self.level_statistics = level_statistics
        for key in self.stats.keys():
            self.stats[key].obj.configure(textvariable=self.level_statistics.stats_str_vars[key])
        self.heatmap_text.set("Mistakes heatmap:\n{}"
                              .format('\n'.join(self.level_statistics.mistakes_heatmap.make_list())))
        self.show_all_objects()
