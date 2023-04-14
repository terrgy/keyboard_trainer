from Object import Object
from scenes.BaseScene import BaseScene
import tkinter as ttk


class MenuScene(BaseScene):
    def __init__(self, app):
        super().__init__(app)

        self.objects.append(Object(
            ttk.Label(self.app, text="Keyboard Trainer", font=("Arial", 30)),
            pack={"pady": 10},
        ))

        self.objects.append(Object(
            ttk.Button(self.app, text="Start", command=self.start_train, font=("Arial", 20)),
            pack={"pady": [30, 10]},
        ))

        self.objects.append(Object(
            ttk.Button(self.app, text="Exit", command=self.app.exit, font=("Arial", 20)),
            pack={"pady": 10},
        ))

    def start_train(self):
        self.app.set_scene(self.app.SCENE_LEVEL_SELECTION)
