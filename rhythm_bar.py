from pico2d import load_image
import game_world
import game_framework

class Rhythm_Bar:
    image = None
    rhythm_perfect = False

    def __init__(self):
        if Rhythm_Bar.image is None:
            Rhythm_Bar.image = load_image('image//rhythm_bar.png')

        self.x1 = 20
        self.velocity = 5  # 속도 설정
        self.x2 = 1580

    def draw(self):
        self.image.clip_draw(0, 0, 190, 144, self.x1, 60, 100, 100)
        self.image.clip_draw(0, 0, 190, 144, self.x2, 60, 100, 100)

    def update(self):
        # 리듬 바의 위치 업데이트
        self.x1 += self.velocity * 100 * game_framework.frame_time
        self.x2 -= self.velocity * 100 * game_framework.frame_time

        # 리듬바가 화면 밖으로 나가면 초기 위치로 재설정
        if  self.x1>=750:
            Rhythm_Bar.rhythm_perfect = True
              # 600에 도달했음을 표시
        elif self.x1< 700:
            Rhythm_Bar.rhythm_perfect = False  # 아직 도달하지 않음
        if self.x1 >= 800:
            self.x1 = 20  # 초기 위치로 재설정
            self.x2 = 1580