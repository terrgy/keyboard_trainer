from typing import List

from Object import Object


class BaseScene:
    def __init__(self, app):
        self.app = app
        self.objects: List[Object] = []

    def show_all_objects(self):
        for obj in self.objects:
            obj.show()

    def hide_all_objects(self):
        for obj in self.objects:
            obj.hide()

    def on_activate(self, *args, **kwargs):
        self.show_all_objects()

    def on_deactivate(self):
        self.hide_all_objects()
