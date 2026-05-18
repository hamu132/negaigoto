# 使う機能だけをカンマ区切りで指名手配する
from manim import *
from timeline import MusicTimeline
from PIL import Image
import numpy as np
import colorsys


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
    def construct(self):
        #self.debug()
        music = MusicTimeline(bpm=150, beats_per_bar=4, offset=1.5)
        


        # 🌊 波を動かすための設定パラメータ
        WAVE_SPEED = 1.0       # 波の流れる速度（大きくすると速くなります）
        WAVE_FREQUENCY = 0.6   # 波の細かさ（メソッドと同じ値にするのがおすすめ）
        WAVE_MIN_BRIGHT = 0.3  # 最も暗い時の輝度（メソッドと同じ値）
        SPARKLE_SPEED = 1.0     # 光の反射がチカチカする速さ（大きいほど素早くきらめきます）
        SPARKLE_INTENSITY = 0.1 # きらめきの強さ（0.2なら、本来の明るさから±20%の範囲で微振動する）
        # phi: 上下の傾き（俯角）, theta: 左右の回転角
        self.set_camera_orientation(phi=75 * DEGREES, theta=-100 * DEGREES)
        sea_dots, sea_data_map = self.create_pixel_sea(
            image_path="img/image.png",
            sky_ratio=0.37,
            dot_x=100,
            dot_y=30,
            wave_frequency=WAVE_FREQUENCY,
            wave_min_bright=WAVE_MIN_BRIGHT
        )

        # 2. 生成したドットをグループにまとめる
        # まとめておくことで、アニメーションの管理が楽になります
        sea_group = VGroup(*sea_dots)
        self.add(sea_group)



        # 3. 経過時間を記録するための変数（内部バッファ）
        self.current_time = 0.0

        # 4. 【超重要】毎フレーム実行される「動きのルール」を定義する（Updater）
        def update_wave(group, dt):
            # dt は「前のフレームから何秒経ったか（約 1/60 秒）」が入ってきます
            self.current_time += dt

            cycle_phase = np.sin(self.current_time * 0.5)
            current_min_bright = interpolate(0.2, 0.5, (cycle_phase + 1.0) / 2.0)
            current_max_bright = interpolate(0.8, 1.0, np.cos(self.current_time * 0.5 + 1.0))
            
            # グループ内の長方形を1つずつループ処理して色を塗り替える
            for rect in group:
                # 事前に rect.id に保存しておいた y_local（何行目か）を取得
                rect_data = sea_data_map[rect]
                x_local = rect_data["id_x"]
                y_local = rect_data["id_y"]
                base_h, base_l, base_s = rect_data["base_hls"]
                sparkle_offset = rect_data["sparkle_offset"]

                sea_rows = rect_data["total_sea_rows"]
                if y_local < (sea_rows * 0.02):
                    rect.set_fill(color=rgb_to_hex(colorsys.hls_to_rgb(base_h, base_l, base_s)))
                    continue

                # 🌊 【数式の魔法】時間に WAVE_SPEED を掛け算して足すことで、波が下へ流れる！
                sin_wave = np.sin(y_local * WAVE_FREQUENCY - self.current_time * WAVE_SPEED)
                wave_factor = interpolate(current_min_bright, current_max_bright, (sin_wave + 1.0) / 2.0)
                
                sparkle_sin = np.sin(self.current_time * SPARKLE_SPEED + sparkle_offset)
                sparkle_factor = 1.0 + (sparkle_sin * SPARKLE_INTENSITY)
                
                total_factor = wave_factor * sparkle_factor
                
                # 新しい輝度を計算して色を上書き
                new_l = base_l * total_factor
                new_l = min(max(new_l, 0.0), 1.0)
                
                new_r, new_g, new_b = colorsys.hls_to_rgb(base_h, new_l, base_s)
                new_color = rgb_to_hex((new_r, new_g, new_b))
                
                # 長方形の色をリアルタイム更新
                rect.set_fill(color=new_color)

        # 5. グループに動くルール（アップデーター）を登録
        sea_group.add_updater(update_wave)

        # 6. 動画を再生する（ただ待つだけで、裏でアップデーターが動き続けます）
        # ボカロの曲の長さに合わせてここを調整します
        self.wait(25)

        # アニメーションを止めたいときはクリアします
        sea_group.clear_updaters()


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