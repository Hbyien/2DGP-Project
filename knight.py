
from pico2d import load_image, clamp, draw_rectangle, get_canvas_width, get_canvas_height

import time

import game_world
import game_framework
from slash_effect import Slash_Effect
from fire_ball import Fire_Ball
from state_machine import (StateMachine, space_down, right_down, right_up, left_down, left_up, start_event, c_down, f_down)

import rhythm_bar
import server
from server import stage
from qblock import Qblock

BOTTOM = 250

#RUN SPEED
PIXEL_PER_METER = (10.0/0.3)
RUN_SPEED_KMPH= 50.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0/ 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM/ 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

#Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0/ TIME_PER_ACTION
FRAMES_PER_ACTION = 6


class Idle:
    @staticmethod
    def enter(knight, e):
        if Slash.is_Slash:
            return
        if Fire.is_Fire:
            return
        elif Jump.is_Jump:
            return

        else:
            knight.dir = 0
            knight.frame = 0


    @staticmethod
    def exit(knight, e):
        if c_down(e):
            Slash.enter(knight, e)
        elif f_down(e):
            Fire.enter(knight,e)

        elif space_down(e):
            Jump.enter(knight, e)
        pass

    @staticmethod
    def do(knight):
        if Slash.is_Slash:
            Slash.do(knight)
        elif Fire.is_Fire:
            Fire.do(knight)
        elif Jump.is_Jump:
            Jump.do(knight)
        else:
            knight.frame = (knight.frame + FRAMES_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time) % 4

    @staticmethod
    def draw(knight):
        if Slash.is_Slash:
            Slash.draw(knight)
        elif Fire.is_Fire:
            Fire.draw(knight)
        elif Jump.is_Jump:
            Jump.draw(knight)
        else:
            if knight.face_dir == 1:
                knight.character_idle.clip_draw(int(knight.frame) * 94, 0, 94, 101, knight.sx, knight.sy)
            else:
                knight.character_idle.clip_composite_draw(int(knight.frame) * 94, 0, 94, 101, 0, 'h', knight.sx, knight.sy, 100, 100)


class Run:
    @staticmethod
    def enter(knight, e):
        if not Slash.is_Slash and not Jump.is_Jump:
            knight.frame = 0
        if right_down(e) or left_up(e):
            knight.dir, knight.face_dir = 1, 1
        elif left_down(e) or right_up(e):
            knight.dir, knight.face_dir = -1, -1


    @staticmethod
    def exit(knight, e):

        if c_down(e):
            Slash.enter(knight, e)

        elif space_down(e):
            Jump.enter(knight, e)
        pass

    @staticmethod
    def do(knight):
        if Slash.is_Slash:
            Slash.do(knight)
        elif Jump.is_Jump:
            Jump.do(knight)
        else:
            knight.x += knight.dir* RUN_SPEED_PPS * game_framework.frame_time
            #knight.x = clamp(10,knight.x, 1190)

            knight.frame = (knight.frame + FRAMES_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time) % 6




    @staticmethod
    def draw(knight):
        if Slash.is_Slash:
            Slash.draw(knight)
        elif Jump.is_Jump:
            Jump.draw(knight)
        else:
            if knight.face_dir == 1:
                knight.character_walk.clip_draw(int(knight.frame) * 96, 0, 96, 94, knight.sx, knight.sy)
            else:
                knight.character_walk.clip_composite_draw(int(knight.frame) * 96, 0, 96, 94, 0, 'h', knight.sx, knight.sy, 100, 100)


class Jump:
    is_Jump = False
    velocity = 10
    gravity = 2
    jump_frame = 0

    @staticmethod
    def enter(knight, e):
        #if rhythm_bar.Rhythm_Bar.rhythm_perfect:

            if not Jump.is_Jump : # 점프 중이 아닐 때만 초기화
                knight.frame = 0
                Jump.velocity = 10  # 점프 속도를 초기화
                Jump.is_Jump = True
                knight.bottom_collide = False

    @staticmethod
    def exit(knight, e):
        Jump.is_Jump = False  # 점프 상태를 초기화

    @staticmethod
    def do(knight):

        # 수직 이동: 점프 속도와 중력 적용
        knight.y += Jump.velocity ** 2 * 0.02 * Jump.gravity * (-1 if Jump.velocity < 0 else 1)
        Jump.velocity -= 20 * game_framework.frame_time


        if knight.block_collide == True:
            knight.block_collide = False
        else:
            # 수평 이동: 점프 시에도 이동 방향 유지
            knight.x += knight.dir * RUN_SPEED_PPS * 0.5 * game_framework.frame_time  # x 이동 거리를 줄임
            #knight.x = clamp(10, knight.x, 1190)  # 화면 경계 안으로 제한

        if knight.jump_top_collide == True:
            Jump.velocity = -5
            knight.jump_top_collide = False




        # 착지 시 점프 종료
        if knight.y <= BOTTOM:  # 지면 높이에 도달하면
            knight.y = BOTTOM
            Jump.is_Jump = False

    @staticmethod
    def draw(knight):
        # 상승 중이면 0-2 프레임, 하강 중이면 3-4 프레임 사용
        if Jump.velocity > 0:  # 상승 중
            Jump.jump_frame = int(knight.frame) % 3  # 프레임 0-2
        else:  # 하강 중
            Jump.jump_frame = min(3 + int(knight.frame) % 2, 4)  # 프레임 3-4

        # 방향에 따라 점프 애니메이션 출력
        if knight.face_dir == 1:
            knight.character_jump.clip_draw(Jump.jump_frame * 96, 0, 96, 94, knight.sx, knight.sy)
        else:
            knight.character_jump.clip_composite_draw(Jump.jump_frame * 96, 0, 96, 94, 0, 'h', knight.sx, knight.sy, 100, 100)


class Slash:
    is_Slash = False

    @staticmethod
    def enter(knight, e):
        #if rhythm_bar.Rhythm_Bar.rhythm_perfect:
            if not Slash.is_Slash:
                knight.frame = 0

                if right_down(e) or left_down(e):
                    knight.dir, knight.face_dir = 1, 1
                elif left_down(e) or right_up(e):
                    knight.dir, knight.face_dir = -1, -1

                Slash.is_Slash = True
            knight.slash_effect()


    @staticmethod
    def exit(knight, e):
       pass

    @staticmethod
    def do(knight):

        knight.frame = (knight.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if knight.frame >= 2:
            Slash.is_Slash = False
    @staticmethod
    def draw(knight):
        if knight.face_dir == 1:
            knight.character_slash.clip_draw(int(knight.frame) * 93, 0, 93, 100, knight.sx, knight.sy)
        else:
            knight.character_slash.clip_composite_draw(int(knight.frame) * 93, 0, 93, 100, 0, 'h', knight.sx, knight.sy, 100, 100)

class Fire:
    is_Fire = False

    @staticmethod
    def enter(knight, e):
        #if rhythm_bar.Rhythm_Bar.rhythm_perfect:
            if not Slash.is_Slash:
                knight.frame = 0

                if right_down(e) or left_down(e):
                    knight.dir, knight.face_dir = 1, 1
                elif left_down(e) or right_up(e):
                    knight.dir, knight.face_dir = -1, -1

                Fire.is_Fire = True
            knight.fire_ball()


    @staticmethod
    def exit(knight, e):
       pass

    @staticmethod
    def do(knight):

        knight.frame = (knight.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if knight.frame >= 2:
            Slash.is_Slash = False
    @staticmethod
    def draw(knight):
        if knight.face_dir == 1:
            knight.character_slash.clip_draw(int(knight.frame) * 93, 0, 93, 100, knight.sx, knight.sy)
        else:
            knight.character_slash.clip_composite_draw(int(knight.frame) * 93, 0, 93, 100, 0, 'h', knight.sx, knight.sy,
                                                       100, 100)


class Knight:
    def __init__(self):
        #self.x, self.y = 400, BOTTOM
        self.frame = 0
        self.dir = 0
        self.face_dir = 1

        self.sx, self.sy = 0, 0

        self.character_walk = load_image('image//walk.png')
        self.character_idle = load_image('image//idle.png')
        self.character_jump = load_image('image//jump.png')
        self.character_slash = load_image('image//slash.png')

        
        self.jump_top_collide = False
        self.block_collide = False
        self.bottom_collide = False

        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions({
            Idle: { right_down: Run, left_down: Run, left_up :Run, right_up: Run, space_down : Idle, c_down : Idle , f_down: Idle},
            Run : {right_down:Idle, left_down:Idle, right_up:Idle, left_up:Idle, space_down : Run, c_down : Run, f_down: Run}

        })

        #self.x, self.y = get_canvas_width() / 2, get_canvas_height() / 2

        self.x = 400
        self.y = server.stage.h / 2 -115

        self.coin_count = 0

        self.knight_fire = False
        self.current_time = 0.0
    def update(self):
        self.state_machine.update()
        self.x = clamp(25.0, self.x, server.stage.w - 25.0)
        self.y = clamp(25.0, self.y, server.stage.h - 25.0)
        if self.knight_fire == True:
            if self.current_time ==0:
                self.current_time = time.time()

            self.character_walk = load_image('image//walk_fire.png')
            self.character_idle = load_image('image//idle_fire.png')
            self.character_jump = load_image('image//jump_fire.png')
            self.character_slash = load_image('image//slash_fire.png')
            if time.time() - self.current_time >= 3.0:
                self.character_walk = load_image('image//walk.png')
                self.character_idle = load_image('image//idle.png')
                self.character_jump = load_image('image//jump.png')
                self.character_slash = load_image('image//slash.png')
                self.knight_fire = False


    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())
        draw_rectangle(*self.get_bb_top())

        draw_rectangle(*self.get_bb_bottom())

        self.sx = self.x - server.stage.window_left
        self.sy = self.y - server.stage.window_bottom

    def slash_effect(self):
        slash_effect = Slash_Effect(self.sx, self.sy, self.face_dir*15)
        game_world.add_object(slash_effect, 1)
        game_world.add_collision_pair('slash_effect:wmonster', slash_effect, None)
        game_world.add_collision_pair('slash_effect:fly', slash_effect, None)

    def fire_ball(self):
        fire_ball = Fire_Ball(self.sx, self.sy, self.face_dir*15)
        game_world.add_object(fire_ball, 1)
        #game_world.add_collision_pair('slash_effect:wmonster', slash_effect, None)
        #game_world.add_collision_pair('slash_effect:fly', slash_effect, None)


    def get_bb(self):

        return self.sx - 30, self.sy - 35, self.sx + 30, self.sy + 35

    def get_bb_top(self):   #머리 충돌 체크 위한거
        return self.sx - 30, self.sy +40, self.sx + 30, self.sy + 47

    def get_bb_bottom(self): # 발 충돌체크 위한거
        return self.sx - 30, self.sy - 45, self.sx + 30, self.sy - 38

    def handle_collision(self, group, other):


        if group == 'knight:wmonster':
            game_framework.quit()

        if group == 'knight:coin':
            pass

        if group == 'knight:mushroom':
            pass

        if group == 'knight:flower':
            self.knight_fire = True
            pass

        if group == 'knight_top:qblock':

            self.jump_top_collide = True
        if group == 'knight:qblock':
            self.block_collide = True

        if group == 'knight_bottom:qblock':
            self.bottom_collide = True

        pass


