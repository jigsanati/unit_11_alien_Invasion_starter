from pathlib import Path


class Settings:

    def __init__(self):
        self.name: str = 'Alien Invsion'
        self.screen_width = 800
        self.screen_height = 800
        self.FPS = 60
        self.bg_file = Path.cwd() / 'Assets' / 'images' / 'Starbasesnow.png'
