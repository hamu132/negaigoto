# 使う機能だけをカンマ区切りで指名手配する
from manim import *
from timeline import MusicTimeline
from PIL import Image
import numpy as np
import colorsys
from manim.utils.rate_functions import ease_out_quad

class ThreeDLayout(ThreeDScene):
    def debug(self):
        # ==========================================
        # ★ 編集モードの切り替えフラグ
        # デバッグ中は True、本番レンダリング時は False にする
        DEBUG_MODE = True 
        # ==========================================

        if DEBUG_MODE:
            # カスタマイズされた見やすい3D数直線
            axes = ThreeDAxes(
                x_range=[-10, 10, 1],  # [最小値, 最大値, 目盛りの間隔]
                y_range=[-10, 10, 1],
                z_range=[-10, 10, 1],
                x_length=20,
                y_length=20,
                z_length=20,
                axis_config={
                    "stroke_width": 2,       # 線の太さ
                    "include_ticks": True,    # 目盛りの「ひげ（区切り線）」を入れるか
                    "tick_size": 0.1,        # 目盛りのひげの大きさ
                }
            )
            # さらに、軸に「X, Y, Z」というラベル文字や数字（Labels）を自動追加する
            labels = axes.get_axis_labels(x_label="X", y_label="Y", z_label="Z")

            # まとめて画面に追加
            self.add(axes, labels)
    
    def play_lyrics(
        self, 
        text_string: str, 
        font: str = "IPAPGothic",
        font_size: int = 48,
        keep_time: float = 3.0,
        fade_out_time: float = 0.8,
        pos_x: float=0,
        pos_y: float=0,
        pos_z: float=0
    ):
        """
        指定した歌詞を3D空間の指定位置にその場でフェードインさせ、
        指定時間キープしたあとにフェードアウトする。
        """
        # 1. テキストオブジェクトの作成
        lyrics_text = Text(
            text_string, 
            font=font, 
            font_size=font_size,
            fill_color=WHITE,
            fill_opacity=0.9
        )

        lyrics_text.rotate(90 * DEGREES, axis=X_AXIS)
        lyrics_text.rotate(0 * DEGREES, axis=Z_AXIS)


        display_pos = np.array([pos_x, pos_y, pos_z])  
        lyrics_text.move_to(display_pos)

        self.play(
            FadeIn(lyrics_text),
            run_time=1.0,
            rate_func=ease_out_quad
        )

        self.wait(keep_time)

        self.play(
            FadeOut(lyrics_text),
            run_time=fade_out_time
        )
        
    def construct(self):
        #self.debug()
        music = MusicTimeline(bpm=150, beats_per_bar=4, offset=1.5)
        
        DEBUG_MODE = True

        # 🌊 波＆きらめきパラメータをインスタンス変数にして共通化
        self.WAVE_SPEED = 1.0
        self.WAVE_FREQUENCY = 0.6
        self.WAVE_MIN_BRIGHT = 0.3
        self.SPARKLE_SPEED = 1.0
        self.SPARKLE_INTENSITY = 0.1

        # phi: 上下の傾き（俯角）, theta: 左右の回転角
        self.set_camera_orientation(phi=75 * DEGREES, theta=-100 * DEGREES)
        if DEBUG_MODE:
            self.debug()

        # 1. 海の生成
        sea_dots, self.sea_data_map = self.create_pixel_sea(
            image_path="img/image.png",
            sky_ratio=0.37,
            dot_x=200,
            dot_y=30,
            wave_frequency=self.WAVE_FREQUENCY,
            wave_min_bright=self.WAVE_MIN_BRIGHT,
        )
        sea_group = VGroup(*sea_dots)

        if DEBUG_MODE:
            self.add(sea_group)
            sea_group.add_updater(lambda g, dt: self.animate_sea_step(g, dt))

        self.current_time = 0.0

        # ========================================================
        # 🎬 メインのタイムライン
        # ========================================================
        time = music.get_duration_by_beats(4)
        

        self.play_lyrics("藁だらけの",
                         font="IPAMincho",
                         keep_time=music.get_duration_by_beats(5),
                         fade_out_time=0.8,
                         font_size=15,
                         pos_x=2,
                         pos_y=-1,
                         pos_z=0.1)


        self.play_lyrics("海で一人、濡れ衣のまま",
                         font="IPAMincho",
                         keep_time=music.get_duration_by_beats(11),
                         fade_out_time=0.8,
                         font_size=20,
                         pos_x=3,
                         pos_y=-2,
                         pos_z=0.1)

        self.play_lyrics("溺れた君は語る",
                         font="IPAMincho",
                         keep_time=music.get_duration_by_beats(11),
                         fade_out_time=0.8,
                         font_size=25,
                         pos_x=0,
                         pos_y=-4,
                         pos_z=0.1)
        
        self.wait(time)

        if not DEBUG_MODE:
            sea_group.clear_updaters()

    def animate_sea_step(self, group: VGroup, dt: float):
        """毎フレーム呼び出され、大きな波のうねりと個別のきらめきを計算・反映する"""
        self.current_time += dt

        # 大きな波の明度変動範囲を決める
        cycle_phase = np.sin(self.current_time * 0.5)
        current_min_bright = interpolate(0.2, 0.5, (cycle_phase + 1.0) / 2.0)
        current_max_bright = interpolate(0.8, 1.0, np.cos(self.current_time * 0.5 + 1.0))

        # 各ドットの色の塗り替えループ
        for rect in group:
            rect_data = self.sea_data_map[rect]
            y_local = rect_data["id_y"]
            base_h, base_l, base_s = rect_data["base_hls"]
            sparkle_offset = rect_data["sparkle_offset"]
            sea_rows = rect_data["total_sea_rows"]

            # 水平線（上部2%）の保護処理
            if y_local < (sea_rows * 0.02):
                rect.set_fill(color=rgb_to_hex(colorsys.hls_to_rgb(base_h, base_l, base_s)))
                continue

            # 🌊 大きな波のうねり（行単位）
            sin_wave = np.sin(y_local * self.WAVE_FREQUENCY - self.current_time * self.WAVE_SPEED)
            wave_factor = interpolate(current_min_bright, current_max_bright, (sin_wave + 1.0) / 2.0)

            # ✨ 個別のきらめき（完全に独立したパチパチ感）
            sparkle_sin = np.sin(self.current_time * self.SPARKLE_SPEED + sparkle_offset)
            sparkle_factor = 1.0 + (sparkle_sin * self.SPARKLE_INTENSITY)

            total_factor = wave_factor * sparkle_factor

            # 新しい輝度を計算して適用
            new_l = base_l * total_factor
            new_l = min(max(new_l, 0.0), 1.0)

            new_r, new_g, new_b = colorsys.hls_to_rgb(base_h, new_l, base_s)
            new_color = rgb_to_hex((new_r, new_g, new_b))

            rect.set_fill(color=new_color)

    def create_pixel_sea(self, image_path, sky_ratio=0.60, dot_x=32, dot_y=20, wave_frequency=0.8, wave_min_bright=0.3):
        img = Image.open(image_path).convert("RGB")
        img_resized = img.resize((dot_x, dot_y), Image.Resampling.BILINEAR)
        img_data = np.array(img_resized)

        start_y = int(dot_y * sky_ratio)
        sea_rows = dot_y - start_y

        step_width = 14.22 / dot_x
        step_height = 6.0 / sea_rows
        
        GAP_FILLER = 1.05 
        rect_width = step_width * GAP_FILLER
        rect_height = step_height * GAP_FILLER

        rectangles = []
        data_map = {}


        np.random.seed(42)
        for y in range(start_y, dot_y):
            y_local = y - start_y
            
            # 初期状態の波計算
            sin_value = np.sin(y_local * wave_frequency)
            wave_factor = interpolate(wave_min_bright, 1.0, (sin_value + 1.0) / 2.0)

            for x in range(dot_x):
                r, g, b = img_data[y, x]
                if r < 10 and g < 10 and b < 10:
                    continue
                
                h, l, s = colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)
                new_l = l * wave_factor
                new_l = min(max(new_l, 0.0), 1.0)
                
                new_r, new_g, new_b = colorsys.hls_to_rgb(h, new_l, s)
                color = rgb_to_hex((new_r, new_g, new_b))
                
                rect = Rectangle(width=rect_width, height=rect_height, fill_color=color, fill_opacity=0.9, stroke_width=0)
                
                pos_x = -7.11 + (x * step_width) + (step_width / 2)
                pos_y = 0.0 - (y_local * step_height) - (step_height / 2)
                rect.move_to((pos_x, pos_y, 0))

                random_offset = np.random.rand() * 2.0 * np.pi
                # 💡 【今回のポイント】後からアニメーションさせるために、
                # 長方形自体に「ベースの色情報」と「自分の行番号」をタグ付けして持たせておく
                data_map[rect] = {
                    "base_hls": (h, l, s),
                    "id_y": y_local,
                    "id_x": x,
                    "total_sea_rows": sea_rows,
                    "sparkle_offset": random_offset
                }
                rectangles.append(rect)

        return rectangles, data_map