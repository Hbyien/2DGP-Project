import game_framework
import game_world

from pico2d import *

from coin import Coin

import server

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Qblock:
    def __init__(self):
        self.x, self.y = 400, 350
        self.block1_image = load_image('objects//qblock1.png')
        self.block2_image = load_image('objects//qblock2.png')


        self.already_collision = False



    def update(self):
        pass
    def draw(self):
        self.sx = self.x - server.stage.window_left
        self.sy = self.y - server.stage.window_bottom
        self.block1_image.draw(self.sx, self.sy, 50, 50)
        draw_rectangle(*self.get_bb())

        if self.already_collision:
            self.block2_image.draw(self.sx, self.sy - server.stage.window_bottom, 50, 50)



    def get_bb(self):
        self.sx = self.x - server.stage.window_left
        self.sy = self.y - server.stage.window_bottom
        return self.sx-30, self.sy-30, self.sx+30, self.sy+30

    def handle_collision(self, group, other):
        if group == 'knight_top:qblock':
            if self.already_collision == False:
                self.coin()
            self.already_collision = True




        if group == 'knight_bottom:qblock':
            pass

    def coin(self):
        coin = Coin(self.x, self.y)
        game_world.add_object(coin, 1)
        game_world.add_collision_pair('knight:coin', None, coin)

