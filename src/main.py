# 使う機能だけをカンマ区切りで指名手配する
from manim import *
from timeline import MusicTimeline

class MoveSquare(Scene):
    def construct(self):
        music = MusicTimeline(bpm=150, beats_per_bar=4)
        square = Square(color=BLUE, fill_opacity=1)
        square.shift(LEFT)

        self.play(FadeIn(square))
        self.wait(0.5)

        self.play(square.animate.shift(RIGHT * 6), run_time=2.0)
        self.wait(1)