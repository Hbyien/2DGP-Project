import game_framework
import game_world
import random
from pico2d import *

import server



class Brick:
    def __init__(self, x = None, y = None):
        self.x, self.y = x,y
        self.image = load_image('objects//brick.png')



    def update(self):
        pass

    def draw(self):
        self.sx = self.x - server.stage.window_left
        self.sy = self.y - server.stage.window_bottom


        self.image.draw(self.sx, self.sy)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        self.sx = self.x - server.stage.window_left
        self.sy = self.y - server.stage.window_bottom
        return self.sx-25, self.sy-30, self.sx+25, self.sy+30

    def handle_collision(self, group, other):
        if group == 'knight_top:brick':
            game_world.remove_object(self)
            pass


        if group == 'knight_bottom:brick':
            pass
        if group == 'knight:brick':
            pass


