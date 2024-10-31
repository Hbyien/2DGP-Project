from pico2d import load_image
from state_machine import StateMachine, space_down, right_down, right_up, left_down, left_up



class Idle:
    @staticmethod
    def enter(knight, e):
        

class Knight:
    def __init__(self):
        self.x , self.y = 400, 90
        self.frame = 0
        self.jump_frame = 0
        self.dir = 0
        self.velocity = 0
        self.gravity = 0.5
        self.look_right = True
        self.stop = True
        self.is_jumping = False
        self.character_walk = load_image('image//walk.png')
        self.character_idle = load_image('image//idle.png')
        self.character_jump = load_image('image//jump.png')

        self.state_machine = StateMachine(self) # 소년 객체의 state machine 생성
        self.state_machine.start(Idle) # 초기 상태가 Idle


   def update(self):
          self.state_machine.update()

      def handle_event(self, event):
          #event : 입력 이벤트 key, mouse
          #우리가 state machine 전달해줄껀 (  ,  ) - 튜플

          self.state_machine.add_event(('INPUT', event))

      def draw(self):
          self.state_machine.draw()



ef handle_events():
    global running, dir, look_right, stop, is_jumping, velocity

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False

        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False

            elif event.key == SDLK_d:  # 오른쪽 이동
                dir += 1
                stop = False
                look_right = True
            elif event.key == SDLK_a:  # 왼쪽 이동
                dir -= 1
                stop = False
                look_right = False

            elif event.key == SDLK_SPACE and not is_jumping:  # 스페이스바로 점프
                is_jumping = True
                velocity = 15  # 점프 시작 속도
                jump_frame = 0  # 점프 시작 시 프레임 리셋

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_d:  # 오른쪽 보고 멈춤
                dir -= 1
                stop = True
                look_right = True
            elif event.key == SDLK_a:  # 왼쪽 보고 멈춤
                dir += 1
                stop = True
                look_right = False

#--------------------------------


#---------------------------------

while running:
    clear_canvas()

    if is_jumping:
        # 점프 애니메이션
        if velocity > 0:  # 위로 올라가는 중
            jump_frame = min(jump_frame, 2)  # 프레임 0~2 사용
        else:  # 내려오는 중
            jump_frame = max(jump_frame, 3)  # 프레임 3~4 사용

        if look_right:
            character_jump.clip_draw(jump_frame * 96, 0, 96, 94, x, y)
        else:
            character_jump.clip_composite_draw(jump_frame * 96, 0, 96, 94, 0, 'h', x, y, 100, 100)

        # 수직 속도 계산 (점프)
        y += velocity
        velocity -= gravity

        # 점프 프레임 업데이트
        jump_frame += 1
        if velocity > 0 and jump_frame > 2:  # 올라가는 중 1~3 프레임
            jump_frame = 2
        elif velocity <= 0 and jump_frame > 4:  # 내려오는 중 4~5 프레임
            jump_frame = 4

        # 땅에 닿으면 점프 종료
        if y <= 90:
            y = 90
            is_jumping = False
            velocity = 0
            jump_frame = 0  # 점프 프레임 리셋

    else:
        # 움직임/정지 애니메이션
        if stop:
            if look_right:
                character_idle.clip_draw(frame * 94, 0, 94, 101, x, 90)
            else:
                character_idle.clip_composite_draw(frame * 94, 0, 94, 101, 0, 'h', x, 90, 100, 100)
            frame = (frame + 1) % 4
        else:
            if look_right:
                character_walk.clip_draw(frame * 96, 0, 96, 94, x, 90)
            else:
                character_walk.clip_composite_draw(frame * 96, 0, 96, 94, 0, 'h', x, 90, 100, 100)
            frame = (frame + 1) % 6

    update_canvas()
    handle_events()

    # 좌우 이동 (점프 중에도 이동 가능)
    x += dir * 10
    if x > 790:
        x = 790
    elif x < 10:
        x = 10

    delay(0.05)

close_canvas()
