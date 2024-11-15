from pico2d import open_canvas, delay, close_canvas

import play_mode

Map_Width, Map_Height = 1000, 600
open_canvas(Map_Width, Map_Height)
play_mode.init()

#게임 루프

while play_mode.running :
    play_mode.handle_events()
    play_mode.update()
    play_mode.draw()
    delay(0.01)
play_mode.finish()
close_canvas()
