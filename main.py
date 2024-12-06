import game_framework
from pico2d import open_canvas, delay, close_canvas

import play_mode as start_mode #로고 모드를 임포트 하되 이름을 스타트 모드로


Map_Width, Map_Height = 1600, 800


open_canvas(Map_Width, Map_Height)
game_framework.run(start_mode)
close_canvas()
