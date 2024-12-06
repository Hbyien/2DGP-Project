from pico2d import load_image, get_canvas_width, get_canvas_height, clamp

import server

class Stage:
    def __init__(self):
        self.image = load_image('image//stage_one.png')
        self.w, self.h = self.image.w, self.image.h
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()

    def draw(self):
        self.image.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 150)

    def update(self):
        self.window_left = clamp(0, int(server.knight.x) - self.cw // 2, self.w - self.cw - 1)
        self.window_bottom = clamp(0, int(server.knight.y) - self.cw // 2, self.h - self.ch - 1)

    def handle_event(self, event):
        pass