import tkinter as ttk

from scenes.Menu import MenuScene
from scenes.Results import ResultsScene
from scenes.Train import TrainScene


class App(ttk.Tk):
    size = width, height = 1000, 700
    SCENE_MENU = 0
    SCENE_TRAIN = 1
    SCENE_RESULTS = 2
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

        self.scenes = [
            MenuScene(self),
            TrainScene(self),
            ResultsScene(self),
        ]

        self.scenes[self.current_scene_index].on_activate()

    def set_scene(self, index, *args, **kwargs):
        self.scenes[self.current_scene_index].on_deactivate()
        self.current_scene_index = index
        self.scenes[self.current_scene_index].on_activate(*args, **kwargs)