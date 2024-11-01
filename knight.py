from pico2d import load_image
from state_machine import StateMachine, space_down, right_down, right_up, left_down, left_up, start_event


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


        pass


class Jump:
    @staticmethod
    def enter(knight, e):
        pass

    @staticmethod
    def exit(knight, e):
        pass

    @staticmethod
    def do(knight):
        pass

    @staticmethod
    def draw(knight):
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
        self.look_right = True
        self.stop = True
        self.is_jumping = False
        self.character_walk = load_image('image//walk.png')
        self.character_idle = load_image('image//idle.png')
        self.character_jump = load_image('image//jump.png')

        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions({
            Idle: {right_down: Run, left_down: Run, left_up :Run, right_up: Run},
            Run : {right_down:Idle, left_down:Idle, right_up:Idle, left_up:Idle}
        })

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
