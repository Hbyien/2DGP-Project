import random

import game_framework
import game_world

from pico2d import *

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4.0


Bottom = 250
class Wmonster:
    images = None

    def __init__(self):
        self.x, self.y = 1000, Bottom
        self.walk_image = load_image('monsters//wmonster_walk.png')
        self.die_image = load_image('monsters//wmonster_die.png')
        self.frame = 0
        self.dir =1
        self.frame_width, self.frame_height = 372//4, 80

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        if self.x > 1100:
            self.dir = -1
        elif self.x < 800:
            self.dir = 1
        self.x = clamp(800, self.x, 1200)
        pass

    def draw(self):
        if self.dir==-1:
            self.walk_image.clip_composite_draw(int(self.frame) * self.frame_width, 0, self.frame_width, self.frame_height,0, 'h', self.x, self.y, 90, 90)
        elif self.dir ==1:
            self.walk_image.clip_draw(int(self.frame)* self.frame_width, 0, self.frame_width, self.frame_height, self.x, self.y)

        draw_rectangle(*self.get_bb())

    def handle_evenet(self, event):
        pass


    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50



