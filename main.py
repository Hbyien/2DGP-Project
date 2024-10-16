from pico2d import *


open_canvas()
character_walk = load_image('image//walk.png')



def handle_events():
    global running
    global  dir

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False

        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False

            elif event.key == SDLK_d:  #오른쪽이동
                dir +=1
            elif event.key == SDLK_a: #왼쪽이동
                dir -=1

        elif event.type ==SDL_KEYUP:
            if event.key == SDLK_d:  #오른쪽이동
                dir -=1
            elif event.key == SDLK_a: #왼쪽이동
                dir +=1

#--------------------------------
frame = 0
running  = True
x = 800//2
dir = 0

while running:
    clear_canvas()
    character_walk.clip_draw(frame*96, 0, 96, 94, x, 90)
    update_canvas()

    handle_events()

    frame = (frame+1) %6
    x += dir*10
    delay(0.05)

close_canvas()