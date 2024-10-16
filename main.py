from pico2d import *


open_canvas()
character_walk = load_image('image//walk.png')

frame = 0
running  = True

def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

for x in range(0, 800, 10):
    clear_canvas()
    character_walk.clip_draw(frame*96, 0, 96, 94, x, 90)
    update_canvas()

    handle_events()
    if not running:
        break

    frame = (frame+1) %8
    delay(0.05)

close_canvas()