import game_framework
import game_world
import server

from pico2d import *

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4.0


class Coin:
    coin_image = None

    def __init__(self, x, y):
        if Coin.coin_image == None:
            self.coin_image = load_image('objects//coin.png')
        self.x, self.y = x, y +50
        self.frame = 0
        self.frame_width, self.frame_height = 72 // 4, 17
        self.coin_count = 0

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

    def draw(self):
        self.sx = self.x - server.stage.window_left
        self.sy = self.y - server.stage.window_bottom
        self.coin_image.clip_draw(int(self.frame) * self.frame_width, 0, self.frame_width, self.frame_height, self.sx, self.sy, 50, 50)
        #draw_rectangle(*self.get_bb())

    def get_bb(self):
        self.sx = self.x - server.stage.window_left
        self.sy = self.y - server.stage.window_bottom
        return self.sx - 20, self.sy - 20, self.sx + 20, self.sy + 20

    def handle_collision(self, group, other):
        if group == 'knight:coin':
            print("충돌은 함")
            self.coin_count += 1
            print(self.coin_count)
            game_world.remove_object(self)