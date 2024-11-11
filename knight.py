from asyncio import Timeout

from pico2d import load_image, clamp
from state_machine import (StateMachine, space_down, right_down, right_up, left_down, left_up,
                           start_event,time_out, c_down)


class Idle:
    @staticmethod
    def enter(knight, e):
        if Slash.is_Slash:
            return
        elif Jump.is_Jump:
            return
        # if left_up(e) or right_down(e):
        #     knight.face_dir = -1
        # elif right_up(e) or left_down(e) or start_event(e):
        #     knight.face_dir = 1
        else:
            knight.dir = 0
            knight.frame = 0

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
            knight.frame = (knight.frame + 1) % 4

    @staticmethod
    def draw(knight):
        if Slash.is_Slash:
            Slash.draw(knight)
        elif Jump.is_Jump:
            Jump.draw(knight)
        else:
            if knight.face_dir == 1:
                knight.character_idle.clip_draw(knight.frame * 94, 0, 94, 101, knight.x, knight.y)
            else:
                knight.character_idle.clip_composite_draw(knight.frame * 94, 0, 94, 101, 0, 'h', knight.x, knight.y, 100, 100)


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
            knight.x += knight.dir*5
            knight.x = clamp(10,knight.x, 790)
            knight.frame = (knight.frame + 1) % 6




    @staticmethod
    def draw(knight):
        if Slash.is_Slash:
            Slash.draw(knight)
        elif Jump.is_Jump:
            Jump.draw(knight)
        else:
            if knight.face_dir == 1:
                knight.character_walk.clip_draw(knight.frame * 96, 0, 96, 94, knight.x, 90)
            else:
                knight.character_walk.clip_composite_draw(knight.frame * 96, 0, 96, 94, 0, 'h', knight.x, 90, 100, 100)





class Jump:
    is_Jump = False
    velocity = 10
    gravity = 0.5
    jump_frame = 0

    @staticmethod
    def enter(knight, e):
        if not Jump.is_Jump:  # 점프 중이 아닐 때만 초기화
            knight.frame = 0

            # Run 상태에서 수평 방향을 유지
            if right_down(e) or left_down(e):
                knight.dir, knight.face_dir = 1, 1
            elif left_down(e) or right_up(e):
                knight.dir, knight.face_dir = -1, -1

            Jump.velocity = 10  # 점프 속도를 리셋하여 반복 점프 가능하게 설정
            Jump.is_Jump = True

    @staticmethod
    def exit(knight, e):
        pass

    @staticmethod
    def do(knight):
        # 점프 속도에 따라 위로 이동
        knight.y += Jump.velocity
        Jump.velocity -= Jump.gravity  # 중력 적용하여 속도 감소

        # Run 상태에서 포물선 경로를 만들기 위한 수평 이동
        knight.x += knight.dir * 5
        knight.x = clamp(10, knight.x, 790)

        # 착지 시 점프 종료
        if knight.y <= 90:
            knight.y = 90
            Jump.is_Jump = False

    @staticmethod
    def draw(knight):
        # 상승 또는 하강 여부에 따라 프레임 결정
        if Jump.velocity > 0:  # 상승 중
            Jump.jump_frame = min(Jump.jump_frame, 2)  # 프레임 0–2 사용
        else:  # 하강 중
            Jump.jump_frame = max(Jump.jump_frame, 3)  # 프레임 3–4 사용

        if knight.face_dir == 1:
            knight.character_jump.clip_draw(Jump.jump_frame * 96, 0, 96, 94, knight.x, knight.y)
        else:
            knight.character_jump.clip_composite_draw(Jump.jump_frame * 96, 0, 96, 94, 0, 'h', knight.x, knight.y, 100, 100)



class Slash:
    is_Slash = False
    slash_timer = 0
    slash_frame_delay = 5
    @staticmethod
    def enter(knight, e):
        if not Slash.is_Slash:
            knight.frame = 0

            if right_down(e) or left_down(e):
                knight.dir, knight.face_dir = 1, 1
            elif left_down(e) or right_up(e):
                knight.dir, knight.face_dir = -1, -1

            Slash.is_Slash = True

    @staticmethod
    def exit(knight, e):
       pass

    @staticmethod
    def do(knight):
        # 슬래시 애니메이션 프레임 지연 적용
        if Slash.slash_timer >= Slash.slash_frame_delay:
            knight.frame = (knight.frame + 1) % 2  # Slash 애니메이션의 2 프레임만 재생
            Slash.slash_timer = 0  # 타이머를 초기화
        else:
            Slash.slash_timer += 1  # 타이머 증가

        # 애니메이션이 끝나면 Slash 상태 종료
        if knight.frame == 0 and Slash.slash_timer == 0:
            Slash.is_Slash = False

    @staticmethod
    def draw(knight):
        if knight.face_dir == 1:
            knight.character_slash.clip_draw(knight.frame * 93, 0, 93, 100, knight.x, knight.y)
        else:
            knight.character_slash.clip_composite_draw(knight.frame * 93, 0, 93, 100, 0, 'h', knight.x, knight.y, 100, 100)

class Knight:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.face_dir = 1
        # self.velocity = 0
        # self.gravity = 0.5
        #self.look_right = True
        #self.stop = True
        #self.is_jumping = False
        self.character_walk = load_image('image//walk.png')
        self.character_idle = load_image('image//idle.png')
        self.character_jump = load_image('image//jump.png')
        self.character_slash = load_image('image//slash.png')


        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions({
            Idle: { right_down: Run, left_down: Run, left_up :Run, right_up: Run, space_down : Idle, c_down : Idle},
            Run : {right_down:Idle, left_down:Idle, right_up:Idle, left_up:Idle, space_down : Run, c_down : Run}

        })

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
