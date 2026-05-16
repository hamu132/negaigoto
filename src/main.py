# 使う機能だけをカンマ区切りで指名手配する
from manim import Scene, Square, LEFT, FadeIn, RIGHT, BLUE

class MoveSquare(Scene):
    def construct(self):
        square = Square(color=BLUE, fill_opacity=0.5)
        square.shift(LEFT * 3)

        self.play(FadeIn(square))
        self.wait(0.5)

        self.play(square.animate.shift(RIGHT * 6), run_time=2.0)
        self.wait(1)