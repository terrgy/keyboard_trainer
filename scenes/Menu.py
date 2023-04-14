from Object import Object
from scenes.BaseScene import BaseScene
import tkinter as ttk


class MenuScene(BaseScene):
    LABEL_FONT = ("Arial", 30)
    BUTTONS_FONT = ("Arial", 20)

    def __init__(self, app):
        super().__init__(app)

        self.objects.append(Object(
            ttk.Label(self.app, text="Keyboard Trainer", font=self.LABEL_FONT),
            pack={"pady": 10},
        ))

        self.objects.append(Object(
            ttk.Button(self.app, text="Start", command=self.start_train, font=self.BUTTONS_FONT),
            pack={"pady": [30, 10]},
        ))

        self.objects.append(Object(
            ttk.Button(self.app, text="Statistics", command=self.goto_statistics, font=self.BUTTONS_FONT),
            pack={"pady": 10},
        ))

        self.objects.append(Object(
            ttk.Button(self.app, text="Exit", command=self.app.exit, font=self.BUTTONS_FONT),
            pack={"pady": 10},
        ))

    def start_train(self):
        self.app.set_scene(self.app.SCENE_LEVEL_SELECTION)

    def goto_statistics(self):
        self.app.set_scene(self.app.SCENE_STATISTICS)
