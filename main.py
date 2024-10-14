from pico2d import *


open_canvas()
character = load_image('image//walk.png')



def handle_events():
    global running, dir, yir
    global look_right, stop

    # fill here

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        # fill here
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                dir +=1
                stop = False
                look_right = True
            elif event.key == SDLK_LEFT:
                dir -=1
                stop = False
                look_right = False
            elif event.key == SDLK_UP:
                yir+=1
                stop = False
            elif event.key == SDLK_DOWN:
                yir-=1
                stop = False
            elif event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                dir -= 1
                stop = True
                look_right = True
            elif event.key == SDLK_LEFT:
                dir += 1
                stop = True
                look_right = False
            elif event.key == SDLK_UP:
                yir -= 1
                stop = True
            elif event.key == SDLK_DOWN:
                yir += 1
                stop = True

running = True
x = 800 // 2
frame = 0
dir = 0
yir = 0
y = 600//2
look_right = True
stop = True

# fill here
while running :
    clear_canvas()

    if stop == True:
        if look_right == True:
            character.clip_draw(frame * 70, 353, 70, 84, x, y, 150, 150)
        elif look_right == False:
            character.clip_composite_draw(frame * 70, 353, 70, 84, 0, 'h', x, y, 150, 150)
        frame = (frame + 1) % 7
    elif stop == False:
        if look_right == True:
            character.clip_draw(frame * 70, 188, 70, 84, x, y, 150, 150)
        elif look_right == False:
            character.clip_composite_draw(frame * 70, 188, 70, 84, 0, 'h', x, y, 150, 150)
        frame = (frame + 1) % 8

    update_canvas()
    handle_events()

    x+=dir*10
    y += yir*10
    if x>790:
        x -= 10
    elif x<10:
        x+=10
    if y>550:
        y-=10
    elif y<50:
        y+=10

    delay(0.05)

close_canvas()

