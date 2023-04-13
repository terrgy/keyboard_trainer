class Object:
    def __init__(self, obj, pack=None, place=None, grid=None):
        self.obj = obj
        self.pack, self.place, self.grid = pack, place, grid

    def set_position(self, pack=None, place=None, grid=None):
        self.pack, self.place, self.grid = pack, place, grid

    def show(self):
        if self.pack:
            self.obj.pack(**self.pack)
        elif self.place:
            self.obj.place(**self.place)
        elif self.grid:
            self.obj.grid(**self.grid)
        else:
            self.obj.pack()

    def hide(self):
        self.obj.pack_forget()
        self.obj.place_forget()
        self.obj.grid_forget()
