
from pico2d import load_image, clamp, draw_rectangle, get_canvas_width, get_canvas_height, load_font

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
from brick import Brick

BOTTOM = 270

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
        elif Fire.is_Fire:
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
        elif knight.block_collide == True:
            if knight.dir ==1:
                knight.x-=5
            elif knight.dir == -1:
                knight.x +=5
            knight.block_collide = False
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
                knight.character_idle.clip_draw(int(knight.frame) * 94, 0, 94, 101, knight.sx, knight.sy, knight.large_x, knight.large_y)
            else:
                knight.character_idle.clip_composite_draw(int(knight.frame) * 94, 0, 94, 101, 0, 'h', knight.sx, knight.sy, knight.large_x, knight.large_y)


class Run:
    @staticmethod
    def enter(knight, e):
        if not Slash.is_Slash and not Jump.is_Jump:
            knight.frame = 0
        if not Fire.is_Fire and not Jump.is_Jump:
            knight.frame = 0
        if right_down(e) or left_up(e):
            knight.dir, knight.face_dir = 1, 1
        elif left_down(e) or right_up(e):
            knight.dir, knight.face_dir = -1, -1


    @staticmethod
    def exit(knight, e):

        if c_down(e):
            Slash.enter(knight, e)
        elif f_down(e):
            Fire.enter(knight,e)

        elif space_down(e):
            Jump.enter(knight, e)


    @staticmethod
    def do(knight):
        if Slash.is_Slash:
            Slash.do(knight)
        elif Fire.is_Fire:
            Fire.do(knight)
        elif Jump.is_Jump:
            Jump.do(knight)

        elif knight.block_collide == True:
            if knight.dir ==1:
                knight.x-=5
            elif knight.dir == -1:
                knight.x +=5
            knight.block_collide = False
        else:
            knight.x += knight.dir* RUN_SPEED_PPS * game_framework.frame_time
            #knight.x = clamp(10,knight.x, 1190)

            knight.frame = (knight.frame + FRAMES_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time) % 6




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
                knight.character_walk.clip_draw(int(knight.frame) * 96, 0, 96, 94, knight.sx, knight.sy, knight.large_x, knight.large_y)
            else:
                knight.character_walk.clip_composite_draw(int(knight.frame) * 96, 0, 96, 94, 0, 'h', knight.sx, knight.sy, knight.large_x, knight.large_y)


class Jump:
    is_Jump = False
    velocity = 10
    gravity = 2
    jump_frame = 0

    @staticmethod
    def enter(knight, e):
        if rhythm_bar.Rhythm_Bar.rhythm_perfect:

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
        knight.y += Jump.velocity ** 2 * 0.03 * Jump.gravity * (-1 if Jump.velocity < 0 else 1)
        Jump.velocity -= 20 * game_framework.frame_time


        if knight.block_collide == True:
            if knight.dir ==1:
                knight.x-=5
            elif knight.dir == -1:
                knight.x +=5
            knight.block_collide = False
        else:
            # 수평 이동: 점프 시에도 이동 방향 유지
            knight.x += knight.dir * RUN_SPEED_PPS * 0.7 * game_framework.frame_time  # x 이동 거리를 줄임


        if knight.jump_top_collide == True:
            Jump.velocity = -5
            knight.jump_top_collide = False

        # stage랑 충돌시 점프 종료
        if Jump.is_Jump == True:
            if knight.bottom_collide == True:

                knight.y = knight.bottom_collide_y +5
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
            knight.character_jump.clip_draw(Jump.jump_frame * 96, 0, 96, 94, knight.sx, knight.sy, knight.large_x, knight.large_y)
        else:
            knight.character_jump.clip_composite_draw(Jump.jump_frame * 96, 0, 96, 94, 0, 'h', knight.sx, knight.sy, knight.large_x, knight.large_y)


class Slash:
    is_Slash = False

    @staticmethod
    def enter(knight, e):
        if rhythm_bar.Rhythm_Bar.rhythm_perfect:
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
            knight.character_slash.clip_draw(int(knight.frame) * 93, 0, 93, 100, knight.sx, knight.sy, knight.large_x, knight.large_y)
        else:
            knight.character_slash.clip_composite_draw(int(knight.frame) * 93, 0, 93, 100, 0, 'h', knight.sx, knight.sy, knight.large_x, knight.large_y)

class Fire:
    is_Fire = False

    @staticmethod
    def enter(knight, e):
        if rhythm_bar.Rhythm_Bar.rhythm_perfect:
            if knight.knight_fire == True:
                if not Fire.is_Fire:
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
            Fire.is_Fire = False

    @staticmethod
    def draw(knight):
        if knight.face_dir == 1:
            knight.character_slash.clip_draw(int(knight.frame) * 93, 0, 93, 100, knight.sx, knight.sy)
        else:
            knight.character_slash.clip_composite_draw(int(knight.frame) * 93, 0, 93, 100, 0, 'h', knight.sx, knight.sy,
                                                       100, 100)


class Knight:
    knight_mushroom = False

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
        self.heart = load_image('objects//heart.png')
        self.coin = load_image('objects//coin_1.png')

        self.font = load_font('ENCR10B.TTF', 40)

        
        self.jump_top_collide = False
        self.block_collide = False
        self.bottom_collide = False
        self.bottom_collide_y =0

        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions({
            Idle: { right_down: Run, left_down: Run, left_up :Run, right_up: Run, space_down : Idle, c_down : Idle , f_down: Idle},
            Run : {right_down:Idle, left_down:Idle, right_up:Idle, left_up:Idle, space_down : Run, c_down : Run, f_down: Run}

        })

        #self.x, self.y = get_canvas_width() / 2, get_canvas_height() / 2

        self.x = 5000
        self.y = server.stage.h / 2 -110

        self.coin_count = 0

        self.knight_fire = False
        self.current_time = 0.0
        self.life =3

        self.large_x, self.large_y = 100, 100
        self.by = 45
        self.by2 = 38
        self.b1 = 30
        self.b2 = 35



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
            if time.time() - self.current_time >= 10.0:
                self.character_walk = load_image('image//walk.png')
                self.character_idle = load_image('image//idle.png')
                self.character_jump = load_image('image//jump.png')
                self.character_slash = load_image('image//slash.png')
                self.knight_fire = False

        if Knight.knight_mushroom == True:
            if self.current_time ==0:
                self.current_time = time.time()
            self.large_x, self.large_y = 200, 200
            #game_world.add_collision_pair('knight_big:brick', server.knight, None)
            #game_world.add_collision_pair('knight_big:qblock', server.knight, None)
            self.by = 78
            self.by2 = 68
            self.b1 = 60
            self.b2 = 70

            if time.time() - self.current_time >= 2.0:
                self.large_x, self.large_y = 100, 100

                self.by = 45
                self.by2 = 38
                self.b1 = 30
                self.b2 = 35
                Knight.knight_mushroom = False
        self.bottom_collide = False
        self.bottom_collide_y = 0
        #Knight.knight_mushroom = False




    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())
        draw_rectangle(*self.get_bb_top())

        draw_rectangle(*self.get_bb_bottom())
        # if self.knight_mushroom == True:
        #     # draw_rectangle(*self.get_bb_big())
        #     # draw_rectangle(*self.get_bb_bottom_big())

        self.sx = self.x - server.stage.window_left
        self.sy = self.y - server.stage.window_bottom

        self.heart_draw()
        self.coin_draw()


    def heart_draw(self):
        if self.life >= -29:
            self.heart.draw(130, 750, 80,80)
        if self.life >= -34:
            self.heart.draw(80, 750, 80, 80)
        if self.life >= -37:
            self.heart.draw(30, 750, 80, 80)

    def coin_draw(self):
        self.coin.draw(200, 750, 50, 50)
        self.font.draw(250, 750, f'{self.coin_count}', (255, 255, 0))
    def slash_effect(self):
        slash_effect = Slash_Effect(self.sx, self.sy, self.face_dir*15)
        game_world.add_object(slash_effect, 1)
        game_world.add_collision_pair('slash_effect:wmonster', slash_effect, None)
        game_world.add_collision_pair('slash_effect:fly', slash_effect, None)

    def fire_ball(self):
        fire_ball = Fire_Ball(self.sx, self.sy, self.face_dir*15)
        game_world.add_object(fire_ball, 1)
        game_world.add_collision_pair('fire_ball:wmonster', fire_ball, None)
        game_world.add_collision_pair('fire_ball:fly', fire_ball, None)


    def get_bb(self):
        return self.sx - self.b1, self.sy - self.b2, self.sx + self.b1, self.sy + self.b2

    def get_bb_big(self):
        return self.sx - 60, self.sy - 70, self.sx + 60, self.sy + 70
    def get_bb_top(self):   #머리 충돌 체크 위한거
        return self.sx - 25, self.sy +40, self.sx + 25, self.sy + 47

    def get_bb_bottom(self): # 발 충돌체크 위한거
        return self.sx - 25, self.sy -self.by, self.sx + 25, self.sy - self.by2
    def get_bb_bottom_big(self): # 발 충돌체크 위한거
        return self.sx - 50, self.sy - 90, self.sx + 50, self.sy - 76

    def handle_collision(self, group, other):


        if group == 'knight:wmonster':
            if Knight.knight_mushroom == True:
                pass
            else:
                self.life-= 1
                self.x = 400
                self.y = server.stage.h / 2 - 110

        if group == 'knight:fly':
            if Knight.knight_mushroom == True:
                pass
            else:
                self.life -= 1
                self.x = 400
                self.y = server.stage.h / 2 - 110

        if group == 'knight:coin':
            self.coin_count += 1
            print(self.coin_count)
            pass

        if group == 'knight:mushroom':
            Knight.knight_mushroom = True
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
            self.bottom_collide_y = self.sy

        if group == 'knight_top:brick':
            self.jump_top_collide = True

        if group == 'knight:brick':
            self.block_collide = True


        if group == 'knight_bottom:brick':
            self.bottom_collide = True
            self.bottom_collide_y = self.sy

        if group == 'knight:stage':
            self.block_collide = True

        if group == 'knight_bottom:stage':
            self.bottom_collide = True
            self.bottom_collide_y = self.sy
            pass


            pass
        pass


