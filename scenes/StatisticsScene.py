from Object import Object
from scenes.BaseScene import BaseScene
import tkinter as ttk


class StatisticsScene(BaseScene):
    FONT = ("Arial", 20)
    STATS_COUNT = 10

    def __init__(self, app):
        super().__init__(app)

        self.text_label = Object(
            ttk.Label(text="Last 10 trains", font=self.FONT)
        )
        self.buttons = list()
        for i in range(self.STATS_COUNT):
            self.buttons.append(Object(
                ttk.Button(text="{})".format(i + 1), font=self.FONT, command=self.make_chooser(i))
            ))
        self.back_to_menu_button = Object(
            ttk.Button(text="Back to menu", font=self.FONT, command=self.back_to_menu)
        )

        self.objects.extend([self.text_label, self.back_to_menu_button])
        self.objects.extend(self.buttons)

    def make_chooser(self, index):
        def chooser():
            self.choose_stat(index)
        return chooser

    def choose_stat(self, index):
        self.app.set_scene(self.app.SCENE_RESULTS, self.app.statistics_manager.stats[index])

    def back_to_menu(self):
        self.app.set_scene(self.app.SCENE_MENU)

    def on_activate(self):
        self.text_label.show()
        for i in range(min(self.STATS_COUNT, self.app.statistics_manager.get_stats_count())):
            self.buttons[i].show()
        self.back_to_menu_button.show()