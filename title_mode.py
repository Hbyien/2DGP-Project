from pico2d import load_image, clear_canvas, update_canvas, get_events, draw_rectangle, load_music
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDLK_UP, SDLK_DOWN

import game_framework
import play_mode



def init():
    global image, current_bb, bgm
    image = load_image('image//choice.png')
    current_bb = None  # 현재 선택된 bounding box
    bgm = load_music('choice.mp3')
    bgm.set_volume(32)
    bgm.repeat_play()

def finish():
    global image
    del image

def handle_events():
    global current_bb
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_SPACE:
                if current_bb == get_bb():
                    game_framework.change_mode(play_mode)
                elif current_bb == get_bb_2():
                    game_framework.change_mode(play_mode)
            elif event.key == SDLK_UP:
                current_bb = get_bb()
            elif event.key == SDLK_DOWN:
                current_bb = get_bb_2()

def get_bb():
    return 400, 500, 1100, 700

def get_bb_2():
    return 400, 150, 1100, 350

def draw():
    clear_canvas()
    image.draw(800, 400)
    if current_bb:
        draw_rectangle(*current_bb)
    update_canvas()

def update():
    pass