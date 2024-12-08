import game_framework
import game_world
import server

from pico2d import *



class Mushroom:
    mushroom_image = None

    def __init__(self, x, y):
        if Mushroom.mushroom_image == None:
            self.mushroom_image = load_image('objects//mushroom.png')
        self.x, self.y = x, y +50

    def update(self):
        pass
    def draw(self):
        self.sx = self.x - server.stage.window_left
        self.sy = self.y - server.stage.window_bottom
        self.mushroom_image.draw(self.sx, self.sy, 40, 50)
        #draw_rectangle(*self.get_bb())

    def get_bb(self):
        self.sx = self.x - server.stage.window_left
        self.sy = self.y - server.stage.window_bottom
        return self.sx - 20, self.sy - 20, self.sx + 20, self.sy + 20

    def handle_collision(self, group, other):
        if group == 'knight:mushroom':
            game_world.remove_object(self)