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
        self.die_frame_width, self.die_frame_height = 507//5, 91
        self.dying = False
        self.die_frame = 0
        self.die_frame_time = 0.0
        self.extra_time = 1.0
        self.is_extra_time_active = False

    def update(self):
        if self.dying:
            self.die_frame_time += game_framework.frame_time
            if not self.is_extra_time_active:  # extra_time 시작 전 프레임 관리
                if self.die_frame_time >= 0.1:  # 각 프레임의 지속 시간: 0.1초
                    self.die_frame += 1
                    self.die_frame_time = 0.0

                if self.die_frame >= 5:  # 모든 프레임이 재생되면 extra_time 활성화
                    self.is_extra_time_active = True
                    self.die_frame = 4  # 마지막 프레임을 유지

                # extra_time 감소
            if self.is_extra_time_active:
                self.extra_time -= game_framework.frame_time
                if self.extra_time <= 0:
                    game_world.remove_object(self)
            return

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        if self.x > 1100:
            self.dir = -1
        elif self.x < 800:
            self.dir = 1
        self.x = clamp(800, self.x, 1200)
        pass

    def draw(self):
        if self.dying:  # 죽는 상태에서는 die_image를 그림
            if self.die_frame < 5:  # die_image의 프레임 재생
                if self.dir == 1:
                    self.die_image.clip_draw(self.die_frame * self.die_frame_width, 0, self.die_frame_width, self.die_frame_height, self.x, self.y)
                elif self.dir == -1:
                    self.die_image.clip_composite_draw(self.die_frame * self.die_frame_width, 0, self.die_frame_width, self.die_frame_height, 0, 'h', self.x, self.y, 90, 90 )
        else :
            if self.dir==-1:
                self.walk_image.clip_composite_draw(int(self.frame) * self.frame_width, 0, self.frame_width, self.frame_height,0, 'h', self.x, self.y, 90, 90)
            elif self.dir ==1:
                self.walk_image.clip_draw(int(self.frame)* self.frame_width, 0, self.frame_width, self.frame_height, self.x, self.y)

            draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass


    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50



    def handle_collision(self, group, other):
        if group == 'slash_effect:wmonster' or group == 'fire_ball:wmonster':
            self.dying  = True

        if group =='knight: wmonster':
            game_framework.quit()