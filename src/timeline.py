from manim import *

class MusicTimeline:
    def __init__(self, bpm: float, beats_per_bar: int = 4, offset: float = 0.0):
        """
        bpm: 曲のテンポ (例: 130)
        beats_per_bar: 1小節の中にある拍数 (4拍子なら4)
        offset: イントロ（1小節目1拍目）が始まるまでの空白時間（秒）
        """
        self.bpm = bpm
        self.beats_per_bar = beats_per_bar
        self.offset = offset  # オフセット秒を記憶
        
        # 1拍および1小節あたりの秒数を計算
        self.seconds_per_beat = 60.0 / bpm
        self.seconds_per_bar = self.seconds_per_beat * beats_per_bar

    def get_time(self, bar: int, beat: float = 1.0) -> float:
        """
        指定した「小節目」と「拍目」から、オフセットを考慮した通算秒数を計算する
        """
        total_bars_time = (bar - 1) * self.seconds_per_bar
        total_beats_time = (beat - 1) * self.seconds_per_beat
        
        # 純粋な音楽の時間に、オフセット秒を足す
        return self.offset + total_bars_time + total_beats_time

    def get_duration_by_beats(self, beats: float) -> float:
        """
        指定された「拍数（ビート数）」が、何秒間に相当するかを計算して返す
        例: 2拍分なら beats=2.0, 0.5拍分（8分音符）なら beats=0.5
        """
        return beats * self.seconds_per_beat

    def get_duration_by_bars(self, bars: float) -> float:
        """
        指定された「小節数」が、何秒間に相当するかを計算して返す
        例: 1小節分なら bars=1.0, 4小節分なら bars=4.0
        """
        return bars * self.seconds_per_bar