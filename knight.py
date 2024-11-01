from pico2d import load_image
from state_machine import StateMachine, space_down, right_down, right_up, left_down, left_up, start_event, land_event, right_land, left_land


class Idle:
    @staticmethod
    def enter(knight, e):
        if left_up(e) or right_down(e):
            knight.face_dir = -1
        elif right_up(e) or left_down(e) or start_event(e):
            knight.face_dir = 1
        knight.dir = 0
        knight.frame = 0

    @staticmethod
    def exit(knight, e):
        pass

    @staticmethod
    def do(knight):
        knight.frame = (knight.frame + 1) % 4

    @staticmethod
    def draw(knight):
        if knight.face_dir == 1:
            knight.character_idle.clip_draw(knight.frame * 94, 0, 94, 101, knight.x, knight.y)
        else:
            knight.character_idle.clip_composite_draw(knight.frame * 94, 0, 94, 101, 0, 'h', knight.x, knight.y, 94, 101)


class Run:
    @staticmethod
    def enter(knight, e):
        if right_down(e) or left_up(e):
            knight.dir, knight.face_dir = 1, 1
        elif left_down(e) or right_up(e):
            knight.dir, knight.face_dir = -1, -1
        pass

    @staticmethod
    def exit(knight, e):
        pass

    @staticmethod
    def do(knight):
        knight.x += knight.dir*5
        knight.frame = (knight.frame + 1) % 6

        if knight.x<0:
            knight.x = 10
        elif knight.x>800:
            knight.x = 790
        pass

    @staticmethod
    def draw(knight):
        if knight.face_dir == 1:
            knight.character_walk.clip_draw(knight.frame * 96, 0, 96, 94, knight.x, 90)
        else:
            knight.character_walk.clip_composite_draw(knight.frame * 96, 0, 96, 94, 0, 'h', knight.x, 90, 100, 100)





class Jump_Up: # 위로 점프
    @staticmethod
    def enter(knight, e):
        knight.velocity = 10
        if knight.face_dir ==1:
            knight.dir = 1
        else:
            knight.dir = -1
        pass

    @staticmethod
    def exit(knight, e):
        #knight.is_jumping = False
        knight.velocity = 0
        pass

    @staticmethod
    def do(knight):
        knight.y += knight.velocity  # 위로 이동
        knight.velocity -= knight.gravity  # 중력 적용

        if knight.y <= 90:
            knight.y = 90
            
            knight.state_machine.add_event(('Land', 0))
        pass

    @staticmethod
    def draw(knight):
        if knight.velocity > 0:  # 상승 중
            knight.jump_frame = min(knight.jump_frame, 2)  # 프레임 0–2 사용
        else:  # 하강 중
            knight.jump_frame = max(knight.jump_frame, 3)  # 프레임 3–4 사용

        if knight.face_dir == 1:
            knight.character_jump.clip_draw(knight.jump_frame * 96, 0, 96, 94, knight.x, knight.y)
        else:
            knight.character_jump.clip_composite_draw(knight.jump_frame * 96, 0, 96, 94, 0, 'h', knight.x, knight.y,100, 100)
        pass


class Jump_Move:
    @staticmethod
    def enter(knight, e):
        # knight.is_jumping = True
        knight.velocity = 10
        if knight.face_dir == 1:
            knight.dir = 1
        else:
            knight.dir = -1
        pass

    @staticmethod
    def exit(knight, e):
        # knight.is_jumping = False
        knight.velocity = 0
        pass

    @staticmethod
    def do(knight):
        knight.y += knight.velocity  # 위로 이동
        knight.velocity -= knight.gravity  # 중력 적용
        knight.x += knight.dir * 5
        if knight.y <= 90:
            knight.y = 90
            knight.state_machine.add_event(('Land', 0))
        pass

    @staticmethod
    def draw(knight):
        if knight.velocity > 0:  # 상승 중
            knight.jump_frame = min(knight.jump_frame, 2)  # 프레임 0–2 사용
        else:  # 하강 중
            knight.jump_frame = max(knight.jump_frame, 3)  # 프레임 3–4 사용

        if knight.face_dir == 1:
            knight.character_jump.clip_draw(knight.jump_frame * 96, 0, 96, 94, knight.x, knight.y)
        else:
            knight.character_jump.clip_composite_draw(knight.jump_frame * 96, 0, 96, 94, 0, 'h', knight.x, knight.y, 100, 100)
        pass


class Knight:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.jump_frame = 0
        self.dir = 0
        self.face_dir = 1
        self.velocity = 0
        self.gravity = 0.5
        #self.look_right = True
        #self.stop = True
        #self.is_jumping = False
        self.character_walk = load_image('image//walk.png')
        self.character_idle = load_image('image//idle.png')
        self.character_jump = load_image('image//jump.png')

        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions({
            Idle: {right_down: Run, left_down: Run, left_up :Run, right_up: Run, space_down : Jump_Up},
            Run : {right_down:Idle, left_down:Idle, right_up:Idle, left_up:Idle, space_down : Jump_Move},
            Jump_Up : {land_event : Idle},
            Jump_Move: {land_event : Idle, left_land: Run, right_land : Run}

        })

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
