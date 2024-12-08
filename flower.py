import game_framework
import game_world
import server

from pico2d import *



class Flower:
    flower_image = None

    def __init__(self, x,y):
        if Flower.flower_image == None:
            self.flower_image = load_image('objects//flower.png')
        self.x, self.y = x, y +50

    def update(self):
        pass
    def draw(self):

        self.flower_image.draw(self.sx, self.sy, 40, 50)
        #draw_rectangle(*self.get_bb())

    def get_bb(self):
        self.sx = self.x - server.stage.window_left
        self.sy = self.y - server.stage.window_bottom
        return self.sx - 20, self.sy - 20, self.sx + 20, self.sy + 20

    def handle_collision(self, group, other):
        if group == 'knight:flower':
            game_world.remove_object(self)