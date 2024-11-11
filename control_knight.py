from pico2d import *

import game_world
from knight import Knight
from stage import Stage

Map_Width, Map_Height = 1000, 600
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
    global running
    global knight
    global stage

    running = True


    stage = Stage()
    game_world.add_object(stage, 0)

    knight = Knight()
    game_world.add_object(knight, 1)



def update_world():
    game_world.update()
    pass


def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()


open_canvas(Map_Width, Map_Height)
reset_world()

#게임 루프

while running :
    handle_events()
    update_world()
    render_world()
    delay(0.01)

close_canvas()

