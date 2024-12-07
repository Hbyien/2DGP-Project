from pico2d import load_image, get_canvas_width, get_canvas_height, clamp, draw_rectangle

import server


class Stage:
    def __init__(self):
        self.image = load_image('image//stage1.png')
        self.w, self.h = self.image.w, self.image.h
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.x, self.y = 0, 0



        self.bb_offsets = [
            (0, 100, 3510, 240)
        ]

    def draw(self):
        self.image.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 150)
        # 각 충돌 박스를 그림
        for bb in self.get_bb():
            draw_rectangle(*bb)

    def update(self):
        self.window_left = clamp(0, int(server.knight.x) - self.cw // 2, self.w - self.cw - 1)
        self.window_bottom = clamp(0, int(server.knight.y) - self.cw // 2, self.h - self.ch - 1)

    def handle_event(self, event):
        pass

    def get_bb(self):
        bbs = []
        for offset in self.bb_offsets:
            x1, y1, x2, y2 = offset
            sx1 = self.x + x1 - server.stage.window_left
            sy1 = self.y + y1 - server.stage.window_bottom
            sx2 = self.x + x2 - server.stage.window_left
            sy2 = self.y + y2 - server.stage.window_bottom
            bbs.append((sx1, sy1, sx2, sy2))
        return bbs

    def handle_collision(self, group, other):
        if group == 'knight_bottom:stage':
            pass

