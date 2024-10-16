from pico2d import *


open_canvas()
character_walk = load_image('image//walk.png')

frame = 0
for x in range(0, 800, 10):
    clear_canvas()
    character_walk.clip_draw(frame*96, 0, 96, 94, x, 90)
    update_canvas()
    frame = (frame+1) %8
    delay(0.05)

close_canvas()