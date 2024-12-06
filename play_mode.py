from pico2d import *


import game_framework
import game_world
import title_mode

import server

from coin import Coin
from knight import Knight
from stage import Stage
from rhythm_base import Rhythm_Base
from bounce import Bounce
from rhythm_bar import Rhythm_Bar
from slash_effect import Slash_Effect
from wmonster import Wmonster
from fly import Fly
from coin import Coin
from qblock import Qblock

def handle_events():

    #global dir, look_right, stop, is_jumping, velocity

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()()

        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)

        else:
            if event.type in (SDL_KEYDOWN, SDL_KEYUP):
                server.knight.handle_event(event)

def init():


    server.stage = Stage()
    game_world.add_object(server.stage, 0)

    bounce = Bounce()
    game_world.add_object(bounce, 1)


    rhythm_base = Rhythm_Base()
    game_world.add_object(rhythm_base, 0)

    server.knight = Knight()
    game_world.add_object(server.knight, 1)

    rhythm_bar = Rhythm_Bar()
    game_world.add_object(rhythm_bar, 2)

    wmonster = Wmonster()
    game_world.add_object(wmonster, 1)

    fly = Fly()
    game_world.add_object(fly, 1)

    #coin = Coin()
    #game_world.add_object(coin, 1)

    qblock = Qblock()
    game_world.add_object(qblock, 1)


    game_world.add_collision_pair('slash_effect:wmonster',None,wmonster)
    game_world.add_collision_pair('slash_effect:fly',None,fly)

    #game_world.add_collision_pair('knight:coin', knight, coin)
    game_world.add_collision_pair('knight_top:qblock', server.knight, qblock)
    game_world.add_collision_pair('knight:qblock', server.knight, qblock)

    game_world.add_collision_pair('knight_bottom:qblock', server.knight, qblock)

    game_world.add_collision_pair('knight:coin', server.knight, None)
    game_world.add_collision_pair('knight:mushroom', server.knight, None)
    game_world.add_collision_pair('knight:flower', server.knight, None)

    #game_world.add_collision_pair('knight: wmonster', None,  wmonster)
    #game_world.add_collision_pair('knight: wmonster', knight,  None)



def finish():
    game_world.clear()
    pass

def update():
    game_world.update()
    game_world.handle_collisions()

    #if game_world.collide(slash_effect, wmonster):


    pass


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def pause():
    pass

def resume():
    pass
