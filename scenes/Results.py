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

        self.level_name_var, self.level_completed_var = ttk.StringVar(), ttk.StringVar()
        self.stats = dict()
        self.create_stats()

        self.heatmap_text = ttk.StringVar()
        self.objects.append(Object(
            ttk.Label(textvariable=self.heatmap_text, font=self.font),
            place={'x': self.app.width // 2, 'y': 0}
        ))

    def create_stats(self):
        self.objects.append(Object(
            ttk.Label(textvariable=self.level_name_var, font=self.font),
            grid={"row": 0, "column": 0}
        ))
        self.objects.append(Object(
            ttk.Label(textvariable=self.level_completed_var, font=self.font),
            grid={"row": 1, "column": 0}
        ))
        index = 2
        for stat in self.level_statistics.stats_names:
            self.stats[stat] = Object(
                ttk.Label(font=self.font),
                grid={"row": index, "column": 0},
            )
            index += 1

        self.objects.extend(self.stats.values())

        self.objects.append(Object(
            ttk.Button(text="Back to menu", font=self.font, command=self.return_to_menu),
            grid={'row': index, 'column': 0}
        ))

    def on_activate(self, level_statistics: LevelStatistics):
        self.level_statistics = level_statistics
        for key in self.stats.keys():
            self.stats[key].obj.configure(textvariable=self.level_statistics.stats_str_vars[key])
        self.heatmap_text.set("Mistakes heatmap:\n{}"
                              .format('\n'.join(self.level_statistics.mistakes_heatmap.make_list())))
        self.level_name_var.set("Level:\n{}".format(level_statistics.level_name))
        self.level_completed_var.set("Completed:\n{}".format("Yes" if level_statistics.is_finished else "No"))
        self.show_all_objects()

    def return_to_menu(self):
        self.app.set_scene(self.app.SCENE_MENU)
