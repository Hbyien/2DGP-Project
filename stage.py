from pico2d import load_image

Map_Width, Map_Height = 1200, 600
class Stage:
    def __init__(self):
        self.image = load_image('image//stage1.png')

    def draw(self):
        self.image.draw(Map_Width//2, Map_Height//2)

    def update(self):
        pass