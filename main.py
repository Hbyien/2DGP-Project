from pico2d import *

from knight import Knight


def handle_events():
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


def reset_world():
    global running, dir, look_right, stop, is_jumping, velocity
    global world
    global knight

    running = True
    world = []

    knight = Knight()
    world.append(knight)



def update_world():
    for o in world:
        o.update()
    pass


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


open_canvas()
reset_world()

#게임 루프

while running :
    handle_events()
    update_world()
    render_world()
    delay(0.01)

close_canvas()

