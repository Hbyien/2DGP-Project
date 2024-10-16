from pico2d import *


open_canvas()
character_walk = load_image('image//walk.png')
character_idle = load_image('image//idle.png')



def handle_events():
    global running
    global  dir
    global look_right, stop


    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False

        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False

            elif event.key == SDLK_d:  #오른쪽이동
                dir +=1
                stop = False
                look_right = True
            elif event.key == SDLK_a: #왼쪽이동
                dir -=1
                stop = False
                look_right = False

        elif event.type ==SDL_KEYUP:
            if event.key == SDLK_d:  #오른쪽보고 멈춤
                dir -=1
                stop = True
                look_right = True
            elif event.key == SDLK_a: #왼쪽보고 멈춤
                dir +=1
                stop = True
                look_right = False

#--------------------------------
frame = 0
running  = True
x = 800//2
dir = 0
look_right = True
stop = True

#---------------------------------

while running:
    clear_canvas()
    if stop == True:
        if look_right == True:
            character_idle.clip_draw(frame *94, 0, 94, 101, x, 90)
        elif look_right == False:
            character_idle.clip_composite_draw(frame * 94, 0, 94, 101,  0, 'h', x, 90, 100, 100)

        frame = (frame+1) %4

    elif stop == False:
        if look_right == True:
            character_walk.clip_draw(frame *96, 0, 96, 94, x, 90)
        elif look_right == False:
            character_walk.clip_composite_draw(frame * 96, 0, 96, 94,0, 'h', x, 90, 100, 100)

        frame = (frame + 1) % 6

    update_canvas()
    handle_events()


    x += dir*10
    if x>790:
        x -= 10
    elif x<10:
        x+=10

    delay(0.05)

close_canvas()