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
        self.knight_x = x



    def draw(self):
        if self.velocity >=0:
            self.image.clip_draw(int(self.frame) * self.frame_width, 0, self.frame_width, self.frame_height, self.x,self.y, 30, 30)
        else:
            self.image.clip_composite_draw(int(self.frame) * self.frame_width, 0, self.frame_width, self.frame_height, 0, 'h', self.x,self.y, 30, 30)
        #draw_rectangle(*self.get_bb())


    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += self.velocity * 80 * game_framework.frame_time

        if abs(self.x - self.knight_x) > 800:
            game_world.remove_object(self)

    def get_bb(self):

        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def handle_collision(self, group, other):
        if group == 'fire_ball:wmonster' or group == 'fire_ball:fly':
            game_world.remove_object(self)