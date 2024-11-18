from pico2d import load_image
import rhythm_bar

Map_Width, Map_Height = 1200, 600
class Bounce:
    def __init__(self):
        self.image = load_image('image//bounce.png')
        self.blue_image = load_image('image//bounce_blue.png')

    def draw(self):
        self.image.clip_draw(0, 0, 161, 166 ,600, 100, 60, 60)
        if rhythm_bar.Rhythm_Bar.rhythm_perfect == True:
            self.blue_image.clip_draw(0, 0, 161, 166, 600, 100, 60, 60)

    def update(self):
        pass