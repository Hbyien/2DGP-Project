from pico2d import *

import game_world
import game_framework
import server

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.3
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4.0

class Fire_Ball:
    image = None

    def __init__(self, x = 400, y = 300, velocity = 1):
        if Fire_Ball.image == None:
            Fire_Ball.image = load_image('image//fire_ball.png')
        self.x, self.y , self.velocity = x, y, velocity
        self.frame = 0
        self.frame_width, self.frame_height = 430//4, 103




    def draw(self):
        self.sx = self.x - server.stage.window_left
        self.sy = self.y - server.stage.window_bottom
        self.image.clip_draw(int(self.frame) * self.frame_width, 0, self.frame_width, self.frame_height, self.sx,self.sy, 30, 30)

        draw_rectangle(*self.get_bb())


    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

    def get_bb(self):
        self.sx = self.x - server.stage.window_left
        self.sy = self.y - server.stage.window_bottom
        return self.sx - 10, self.sy - 10, self.sx + 10, self.sy + 10

    def handle_collision(self, group, other):
        pass