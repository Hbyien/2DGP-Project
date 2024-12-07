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
from brick import Brick

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





    #coin = Coin()
    #game_world.add_object(coin, 1)

    coordinates = [(842, 430), (1098, 430), (1198, 430), (1148, 650), (4008, 430), (4827, 650), (5440, 430),
                   (5592, 430), (5745, 430), (5592, 650),(6617, 650),(6668, 650), (8710, 430) ]

    # 리스트를 사용하여 Qblock 생성 및 추가
    for x, y in coordinates:
        qblock = Qblock(x, y)
        game_world.add_object(qblock, 1)
        game_world.add_collision_pair('knight_top:qblock', server.knight, qblock)
        game_world.add_collision_pair('knight:qblock', server.knight, qblock)
        game_world.add_collision_pair('knight_bottom:qblock', server.knight, qblock)
        game_world.add_collision_pair('knight_big:qblock', None, qblock)

    brick_location = [(1046,  430), (1146, 430), (1248, 430), (3957, 430), (4058, 430), (4825, 430), (5132, 430), (5182, 430),
                      (4112, 650),(4162, 650), (4212, 650),(4262,650), (4312, 650),(4362, 650 ), (4162, 650), (4662, 650)
                      , (6051, 430), (6612, 430), (6662, 430), (6206, 650), (6256, 650), (6306, 650),(6561, 650),(6717, 650 ),
                      (8608, 430), (8658, 430), (8760, 430)]
    for x, y in brick_location:
        brick = Brick(x, y)
        game_world.add_object(brick, 1)
        game_world.add_collision_pair('knight_top:brick', server.knight, brick)
        game_world.add_collision_pair('knight:brick', server.knight, brick)
        game_world.add_collision_pair('knight_bottom:brick', server.knight, brick)


    wmonster_location = [(800, 280), (4000, 280), (5350, 280), (6100, 280)]
    for x, y in wmonster_location:
        wmonster = Wmonster(x, y)
        game_world.add_object(wmonster, 1)
        game_world.add_collision_pair('slash_effect:wmonster', None, wmonster)
        game_world.add_collision_pair('fire_ball:wmonster', None, wmonster)
        game_world.add_collision_pair('knight:wmonster', server.knight, wmonster)


    fly_location = [(1715, 300), (2192, 350), (2684, 324), (8971, 324)]
    for x, y in fly_location:
        fly = Fly(x, y)
        game_world.add_object(fly, 1)
        game_world.add_collision_pair('slash_effect:fly', None, fly)
        game_world.add_collision_pair('fire_ball:fly', None, fly)
        game_world.add_collision_pair('knight:fly', server.knight, fly)







    #game_world.add_collision_pair('knight:coin', knight, coin)


    game_world.add_collision_pair('knight:coin', server.knight, None)
    game_world.add_collision_pair('knight:mushroom', server.knight, None)
    game_world.add_collision_pair('knight:flower', server.knight, None)

    game_world.add_collision_pair('knight_bottom:stage', server.knight, server.stage)
    game_world.add_collision_pair('knight:stage', server.knight, server.stage)






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
