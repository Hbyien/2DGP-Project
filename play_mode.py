from pico2d import *

import game_world
from knight import Knight
from stage import Stage
from rhythm_base import Rhythm_Base



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

def init():
    global running
    global knight

    running = True


    stage = Stage()
    game_world.add_object(stage, 0)


    rhythm_base = Rhythm_Base()
    game_world.add_object(rhythm_base, 0)

    knight = Knight()
    game_world.add_object(knight, 1)

def finish():
    pass

def update():
    game_world.update()
    pass


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()



