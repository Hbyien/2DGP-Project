from pico2d import *

from knight import Knight


def handle_events():
    global running, dir, look_right, stop, is_jumping, velocity

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False

        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

        else:
            if event.type in (SDL_KEYDOWN, SDL_KEYUP):
                knight.handle_event(event)

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

