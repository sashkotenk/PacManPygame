class Settings:
    def __init__(self):
        self.resolution = (640, 480)
        self.bg_color = (0, 0, 0)
        self.difficulty = 1

    def set_resolution(self, resolution):
        self.resolution = resolution
        return resolution  

    def adjust_difficulty(self, level):
        self.difficulty = level

    def change_bg_color(self, color):
        self.bg_color = color

