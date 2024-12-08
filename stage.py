from pico2d import load_image, get_canvas_width, get_canvas_height, clamp, draw_rectangle, load_music

import server


class Stage:
    def __init__(self):
        self.image = load_image('image//stage1.png')
        self.w, self.h = self.image.w, self.image.h
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.x, self.y = 0, 0

        self.bgm = load_music('stage1.mp3')
        self.bgm.set_volume(32)
        self.bgm.repeat_play()



        self.bb_offsets = [
            (0, 100, 3510, 240),
            (3625, 100, 4391, 240),
            (4544, 100, 7817, 240),
            (7917, 100, 10700, 240),

            (6844, 100, 6897, 293),
            (6897, 100, 6947, 353),
            (6947, 100, 6997, 403),
            (6997, 100, 7047, 463),

            (7150, 100, 7200, 463),
            (7200, 100, 7250, 403),
            (7250, 100, 7300, 353),
            (7300, 100, 7350, 293),

            (7560, 100, 7610, 293),
            (7610, 100, 7660, 353),
            (7660, 100, 7710, 403),
            (7710, 100, 7760, 463),
            (7760, 100, 7810, 463),

            (7918, 100, 7968, 463),
            (7968, 100, 8018, 403),
            (8018, 100, 8068, 353),
            (8068, 100, 8118, 293),

            (9248, 100, 9298, 293),
            (9298, 100, 9348, 353),
            (9348, 100, 9398, 403),
            (9398, 100, 9448, 463),
            (9448, 100, 9498, 513),
            (9498, 100, 9548, 563),
            (9548, 100, 9598, 623),
            (9598, 100, 9648, 673),
            (9648, 100, 9698, 673),

            (1429, 100, 1529, 350),
            (1941, 100, 2041, 400),
            (2352, 100, 2452, 455),
            (2910, 100, 3010, 455),

            (8327, 100, 8427, 350),
            (9150, 100, 9250, 350)


        ]

    def draw(self):
        self.image.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 150)
        # 각 충돌 박스를 그림
        for bb in self.get_bb():
            draw_rectangle(*bb)
        draw_rectangle(*self.get__bb2())
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

    def get__bb2(self):
        return 10000, 200, 10144, 800

    def handle_collision(self, group, other):
        if group == 'knight_bottom:stage':
            pass

        if group == 'knight:stage':
            pass

        if group == 'knight:flag':
            pass