from Object import Object
from scenes.BaseScene import BaseScene
import tkinter as ttk

from statistics.LevelStatistics import LevelStatistics


class TrainScene(BaseScene):
    TYPE_LETTERS_FONT_SIZE = 30
    TYPE_LETTERS_LEFT_COUNT = 15
    TYPE_LETTERS_RIGHT_COUNT = 15
    TIME_UPDATE_INTERVAL_MS = 100
    MAIN_FONT_SIZE = 30

    class LetterLabelSettings:
        class Statuses:
            NORMAL = 1
            WRONG = 2
            RIGHT = 3
            LEFT_NORMAL = 4
            LEFT_WRONG = 5
            LEFT_RIGHT = 6

            to_left_conversion = {
                NORMAL: LEFT_NORMAL,
                WRONG: LEFT_WRONG,
                RIGHT: LEFT_RIGHT
            }

            @classmethod
            def make_left(cls, status):
                if status in cls.to_left_conversion:
                    return cls.to_left_conversion[status]
                return status

        color_by_status = {
            Statuses.NORMAL: "#000000",
            Statuses.WRONG: "#FF0000",
            Statuses.RIGHT: "#00FF00",
            Statuses.LEFT_NORMAL: "#808080",
            Statuses.LEFT_WRONG: "#FF7373",
            Statuses.LEFT_RIGHT: "#79C479",
        }

        def __init__(self, index, status=Statuses.NORMAL):
            self.index = index
            self.str_var = ttk.StringVar()
            self.status = status

        def copy(self, other):
            self.status = other.status
            if self.index < TrainScene.TYPE_LETTERS_LEFT_COUNT:
                self.status = self.Statuses.make_left(self.status)

            self.str_var.set(other.str_var.get())

        def get_config(self):
            return {'foreground': self.color_by_status[self.status]}

    def __init__(self, app):
        super().__init__(app)

        self.current_level = None
        self.current_text_pos = 0

        self.is_train_started = False
        self.after_timer_id = None
        self.level_statistics = LevelStatistics()

        self.letters_settings, self.letters = list(), list()
        self.create_letters()

        self.stats = dict()
        self.create_stats()

        self.start_label = Object(
            ttk.Label(text="Press Enter to start", font=("Arial", self.MAIN_FONT_SIZE))
        )
        self.objects.append(self.start_label)

    def create_stats(self):
        for c in range(3):
            self.app.columnconfigure(index=c, weight=1)

        font = ("Arial", self.MAIN_FONT_SIZE)
        places = {
            'chars_count': {"row": 0, "column": 0},
            'mistakes': {"row": 0, "column": 1},
            'mistakes_percentage': {"row": 0, "column": 2},
            'elapsed_time': {"row": 1, "column": 0},
            'average_speed': {"row": 1, "column": 2},
        }
        for stat in self.level_statistics.stats_names:
            self.stats[stat] = Object(
                ttk.Label(font=font),
                grid=places[stat],
            )

        self.objects.extend(self.stats.values())

    def update_time(self):
        self.level_statistics.elapsed_time += self.TIME_UPDATE_INTERVAL_MS / 1000
        self.level_statistics.update_str_vars()
        self.after_timer_id = self.app.after(self.TIME_UPDATE_INTERVAL_MS, self.update_time)

    def create_letters(self):
        self.letters_settings = [self.LetterLabelSettings(i)
                                 for i in range(self.TYPE_LETTERS_LEFT_COUNT + self.TYPE_LETTERS_RIGHT_COUNT + 1)]

        letters_start_x = (self.app.width - self.TYPE_LETTERS_FONT_SIZE) // 2 \
                          - self.TYPE_LETTERS_LEFT_COUNT * self.TYPE_LETTERS_FONT_SIZE
        letters_start_y = (self.app.height - self.TYPE_LETTERS_FONT_SIZE) // 2
        for i in range(self.TYPE_LETTERS_LEFT_COUNT + self.TYPE_LETTERS_RIGHT_COUNT + 1):
            params = {
                'textvariable': self.letters_settings[i].str_var
            }
            if i == self.TYPE_LETTERS_LEFT_COUNT:
                params['font'] = ('monospace', self.TYPE_LETTERS_FONT_SIZE, 'bold')
                params['borderwidth'] = 2
                params['relief'] = 'ridge'
            else:
                params['font'] = ('monospace', self.TYPE_LETTERS_FONT_SIZE)

            self.letters.append(Object(
                ttk.Label(**params),
                place={'x': letters_start_x + i * self.TYPE_LETTERS_FONT_SIZE, 'y': letters_start_y}
            ))
        self.objects.extend(self.letters)

    def get_next_char(self):
        if self.current_text_pos >= len(self.current_level.text):
            return ''
        res = self.current_level.text[self.current_text_pos]
        self.current_text_pos += 1
        return res

    def configure_level(self, level_name):
        self.current_level = self.app.levels_manager.get_level(level_name)
        self.current_text_pos = 0

        for i in range(self.TYPE_LETTERS_LEFT_COUNT):
            self.letters_settings[i].str_var.set('')
        for i in range(self.TYPE_LETTERS_LEFT_COUNT, len(self.letters_settings)):
            self.letters_settings[i].str_var.set(self.get_next_char())
            self.letters_settings[i].status = self.LetterLabelSettings.Statuses.NORMAL

        self.level_statistics = LevelStatistics()
        self.level_statistics.level_name = level_name
        self.level_statistics.create_str_vars()

        for key in self.stats.keys():
            self.stats[key].obj.configure(textvariable=self.level_statistics.stats_str_vars[key])

    def on_activate(self, text="Lorem ipsum dolor sit amet, consectetur adipiscing elit,"):
        self.configure_level(text)
        self.start_label.show()
        self.app.bind("<Return>", self.start_train)
        self.app.bind('<Escape>', self.exit_train)

    def start_train(self, event):
        self.app.unbind("<Return>")
        self.start_label.hide()
        for obj in self.letters:
            obj.show()
        for obj in self.stats.values():
            obj.show()
        self.after_timer_id = self.app.after(self.TIME_UPDATE_INTERVAL_MS, self.update_time)
        self.is_train_started = True
        self.app.bind("<KeyPress>", self.key_press_event)

    def update_letter(self, index):
        self.letters[index].obj.config(self.letters_settings[index].get_config())

    def update_all_letters(self):
        for i in range(len(self.letters)):
            self.update_letter(i)

    def shift_letters(self):
        for i in range(len(self.letters) - 1):
            self.letters_settings[i].copy(self.letters_settings[i + 1])
        self.letters_settings[len(self.letters) - 1].str_var.set(self.get_next_char())
        self.letters_settings[len(self.letters) - 1].status = self.LetterLabelSettings.Statuses.NORMAL

    def on_deactivate(self):
        if self.after_timer_id:
            self.app.after_cancel(self.after_timer_id)
        self.app.unbind("<KeyPress>")
        self.app.unbind("<Return>")
        self.app.unbind("<Escape>")
        self.hide_all_objects()

    def exit_train(self, event):
        if self.is_train_started:
            self.app.statistics_manager.add_level_statistics(self.level_statistics)
            self.app.set_scene(self.app.SCENE_RESULTS, self.level_statistics)
        else:
            self.app.set_scene(self.app.SCENE_MENU)

    def key_press_event(self, event):
        if not getattr(event, 'char', None):
            return

        if event.char != self.letters_settings[self.TYPE_LETTERS_LEFT_COUNT].str_var.get():
            if self.letters_settings[self.TYPE_LETTERS_LEFT_COUNT].status != self.LetterLabelSettings.Statuses.WRONG:
                self.letters_settings[self.TYPE_LETTERS_LEFT_COUNT].status = self.LetterLabelSettings.Statuses.WRONG
                self.update_letter(self.TYPE_LETTERS_LEFT_COUNT)
                self.level_statistics.add_mistake(self.letters_settings[self.TYPE_LETTERS_LEFT_COUNT].str_var.get())
        else:
            if self.letters_settings[self.TYPE_LETTERS_LEFT_COUNT].status != self.LetterLabelSettings.Statuses.WRONG:
                self.letters_settings[self.TYPE_LETTERS_LEFT_COUNT].status = self.LetterLabelSettings.Statuses.RIGHT
                self.level_statistics.add_correct(self.letters_settings[self.TYPE_LETTERS_LEFT_COUNT].str_var.get())
            self.shift_letters()
            self.update_all_letters()
        self.level_statistics.update_str_vars()

        if self.letters_settings[self.TYPE_LETTERS_LEFT_COUNT].str_var.get() == '':
            self.level_statistics.is_finished = True
            self.exit_train(None)
