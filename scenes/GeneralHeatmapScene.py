from Object import Object
from scenes.BaseScene import BaseScene
import tkinter as ttk

from statistics.MistakesHeatmap import MistakesHeatmap


class GeneralHeatmapScene(BaseScene):
    FONT = ("Arial", 20)

    def __init__(self, app):
        super().__init__(app)

        self.objects.append(Object(
            ttk.Label(text="General heatmap for trains on the previous screen", font=self.FONT)
        ))

        self.heatmap_var = ttk.StringVar()
        self.objects.append(Object(
            ttk.Label(textvariable=self.heatmap_var, font=self.FONT)
        ))

        self.objects.append(Object(
            ttk.Button(text="Back to statistics", font=self.FONT, command=self.back_to_stats),
            place={"x": 0, "y": self.app.height // 2}
        ))

    def back_to_stats(self):
        self.app.set_scene(self.app.SCENE_STATISTICS)

    def on_activate(self):
        general_heatmap = MistakesHeatmap()
        for stat in self.app.statistics_manager.stats:
            general_heatmap += stat.mistakes_heatmap
        self.heatmap_var.set('\n'.join(general_heatmap.make_list()))
        self.show_all_objects()

