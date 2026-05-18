from manim import *

class MusicTimeline:
    def __init__(self, bpm: float, beats_per_bar: int = 4):
        """
        bpm: 曲のテンポ (例: 130)
        beats_per_bar: 1小節の中にある拍数 (4拍子なら4)
        """
        self.bpm = bpm
        self.beats_per_bar = beats_per_bar
        
        # 1拍（1ビート）あたりの秒数
        self.seconds_per_beat = 60.0 / bpm
        # 1小節あたりの秒数
        self.seconds_per_bar = self.seconds_per_beat * beats_per_bar

    def get_time(self, bar: int, beat: float = 1.0) -> float:
        """
        指定した「小節目」と「拍目」から、曲頭からの通算秒数を計算する
        ※音楽の慣習に合わせて、1小節目、1拍目を基準（1スタート）とします
        """
        total_bars_time = (bar - 1) * self.seconds_per_bar
        total_beats_time = (beat - 1) * self.seconds_per_beat
        return total_bars_time + total_beats_time