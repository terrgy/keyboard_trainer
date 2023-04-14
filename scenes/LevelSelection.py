from Object import Object
from scenes.BaseScene import BaseScene
import tkinter as ttk


class LevelSelectionScene(BaseScene):
    MAIN_FONT_SIZE = 30
    GRID_COLUMNS = 3

    def __init__(self, app):
        super().__init__(app)

        for c in range(self.GRID_COLUMNS):
            self.app.columnconfigure(index=c, weight=1)

        font = ("Arial", self.MAIN_FONT_SIZE)
        current_row, current_column = 0, 0
        for level_name in self.app.levels_manager.get_levels_list():
            self.objects.append(Object(
                ttk.Button(text=level_name, font=font, command=self.make_chooser(level_name)),
                grid={'row': current_row, 'column': current_column}
            ))
            current_column += 1
            if current_column >= self.GRID_COLUMNS:
                current_row += 1
                current_column = 0
        if current_column:
            current_row += 1
        self.objects.append(Object(
            ttk.Button(text='Back to menu', font=font, command=self.back_to_menu),
            grid={'row': current_row, 'column': self.GRID_COLUMNS // 2}
        ))

    def make_chooser(self, level_name):
        def chooser():
            self.choose_level(level_name)
        return chooser

    def choose_level(self, level_name):
        self.app.set_scene(self.app.SCENE_TRAIN, level_name)

    def back_to_menu(self):
        self.app.set_scene(self.app.SCENE_MENU)
