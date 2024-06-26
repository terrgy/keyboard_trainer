import tkinter as ttk

from levels_manager.LevelsManager import LevelsManager
from scenes.GeneralHeatmapScene import GeneralHeatmapScene
from scenes.LevelSelection import LevelSelectionScene
from scenes.Menu import MenuScene
from scenes.Results import ResultsScene
from scenes.StatisticsScene import StatisticsScene
from scenes.Train import TrainScene
from statistics.StatisticsManager import StatisticsManager


class App(ttk.Tk):
    size = width, height = 1000, 700
    SCENE_MENU = 0
    SCENE_TRAIN = 1
    SCENE_RESULTS = 2
    SCENE_LEVEL_SELECTION = 3
    SCENE_STATISTICS = 4
    SCENE_GENERAL_HEATMAP = 5
    current_scene_index = SCENE_MENU

    def __init__(self):
        super().__init__()

        self.resizable(False, False)

        self.geometry("{width}x{height}+{x}+{y}".format(
            width=self.width,
            height=self.height,
            x=int((self.winfo_screenwidth() - self.width) / 2),
            y=int((self.winfo_screenheight() - self.height) / 2)
        ))

        self.title("Keyboard Trainer")

        self.levels_manager = LevelsManager()
        self.statistics_manager = StatisticsManager()

        self.scenes = [
            MenuScene(self),
            TrainScene(self),
            ResultsScene(self),
            LevelSelectionScene(self),
            StatisticsScene(self),
            GeneralHeatmapScene(self),
        ]

        self.scenes[self.current_scene_index].on_activate()

    def set_scene(self, index, *args, **kwargs):
        self.scenes[self.current_scene_index].on_deactivate()
        self.current_scene_index = index
        self.scenes[self.current_scene_index].on_activate(*args, **kwargs)

    def exit(self):
        self.destroy()
