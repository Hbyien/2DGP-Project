from pico2d import load_image

import game_world


class Slash_Effect:
    image = None

    def __init__(self, x = 400, y = 300, velocity = 1):
        if Slash_Effect.image == None:
            Slash_Effect.image = load_image('image//slash_effect.png')

        self.x, self.y , self.velocity = x, y, velocity

    def draw(self):
        if self.velocity>=0:
            self.image.clip_draw(0,0 ,190,144,self.x, self.y)
        else:
            self.image.clip_composite_draw(0, 0, 190, 144, 0, 'h', self.x, self.y, 190, 144)

    def update(self):

        self.x += self.velocity