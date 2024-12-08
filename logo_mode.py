import game_framework
from pico2d import load_image, delay, clear_canvas, update_canvas, get_events, get_time, load_music

import title_mode


def init():
    global image, bgm
    global logo_start_time

    image = load_image('image//title.png')
    logo_start_time = get_time()

    bgm = load_music('title.mp3')
    bgm.set_volume(32)
    bgm.repeat_play()


def finish():
    global image
    del image

def update():

    global logo_start_time
    if get_time() - logo_start_time >= 4.0:
        logo_start_time = get_time()
        game_framework.change_mode(title_mode)

def draw():
    clear_canvas()
    image.draw(800, 400)
    update_canvas()

def handle_events():
    events = get_events()