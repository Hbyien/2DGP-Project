from pico2d import load_image

Map_Width, Map_Height = 1000, 600
class Rhythm_Base:
    def __init__(self):
        self.base_image = load_image('image//black_base.png')


    def do(self):
        self.frame = (self.frame + 1) % 4

    def draw(self):
        self.base_image.draw(Map_Width//2, 40)


    def update(self):
        pass