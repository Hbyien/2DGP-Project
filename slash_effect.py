from pico2d import load_image

import game_world
import game_framework


class Slash_Effect:
    image = None

    def __init__(self, x = 400, y = 300, velocity = 1):
        if Slash_Effect.image == None:
            Slash_Effect.image = load_image('image//slash_effect.png')

        self.x, self.y , self.velocity = x, y, velocity
        self.knight_x = x

    def draw(self):
        if self.velocity>=0:
            self.image.clip_draw(0,0 ,190,144,self.x, self.y, 100, 100)
        else:
            self.image.clip_composite_draw(0, 0, 190, 144, 0, 'h', self.x, self.y, 100, 100)

    def update(self):

        self.x += self.velocity*100*game_framework.frame_time

        if abs(self.x - self.knight_x) > 100:
            game_world.remove_object(self)

