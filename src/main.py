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


    def play_lyrics_move(self, text_string: str, font: str="IPAMincho", font_size: int=15, speed: float=1, pos_x: float=4, pos_y: float=0, pos_z: float=5):
        lyrics_text = Text(text_string, font=font, font_size=font_size, fill_color=WHITE, fill_opacity=0.9)
        lyrics_text.rotate(75 * DEGREES, axis=X_AXIS).rotate(-10 * DEGREES, axis=Z_AXIS)
        lyrics_text.set_z_index(-2)
        start_pos = np.array([pos_x, pos_y, pos_z])
        end_pos = np.array([pos_x, pos_y, pos_z - 6.0]) # Z軸を -6 する
        
        lyrics_text.move_to(start_pos)
        lyrics_text.align_to(start_pos, RIGHT)
        self.add(lyrics_text)

        # 速度計算
        direction = end_pos - start_pos
        distance = np.linalg.norm(direction)
        velocity = (direction / distance) * speed

        def updater_move(m, dt):
            m.shift(velocity * dt)
            if m.get_center()[2] <= end_pos[2]: 
                m.clear_updaters()
                self.remove(m)

        lyrics_text.add_updater(updater_move)

    def set_square(self):
        box = Rectangle(width=30, height=10)
        box.set_fill(color="#000000", opacity=1)
        box.set_stroke(width=0)
        box.move_to(np.array([0, -5.0, 0]))
        box.set_z_index(-1)
        self.add(box)

    def set_moon(self):

        # ==========================================
        # 🌙 基本設定
        # ==========================================

        moon_radius = 2.0

        self.moon_pos = np.array([
            -2.0,
            0,
            6
        ])

        # ==========================================
        # 🌙 月 + グロー画像
        # ==========================================

        self.moon = ImageMobject(
            "img/moon_with_glow.png"
        )

        # ピクセル感維持
        self.moon.set_resampling_algorithm(
            RESAMPLING_ALGORITHMS["nearest"]
        )

        # サイズ調整
        # glow込み画像なので少し大きめに
        self.moon.scale_to_fit_width(
            moon_radius * 6
        )

        # 位置
        self.moon.move_to(
            self.moon_pos
        )

        # カメラ角度
        self.moon.rotate(
            75 * DEGREES,
            axis=RIGHT
        )

        # ==========================================
        # 🌙 シーン追加
        # ==========================================

        self.add(self.moon)

    def set_cloud(self):

        # ==========================================
        # ☁ 雲レイヤー
        # ==========================================

        self.clouds = Group()

        cloud_paths = [

            "img/cloud_01.png",
            "img/cloud_02.png",
            "img/cloud_03.png",
            "img/cloud_04.png"
        ]

        cloud_count = 40

        for _ in range(cloud_count):

            path = np.random.choice(cloud_paths)

            # ==========================================
            # 奥行き
            # ==========================================

            z = np.random.uniform(
                1.8,
                4.5
            )

            depth_t = inverse_interpolate(
                1.8,
                4.5,
                z
            )

            # ==========================================
            # 移動速度
            # 近景ほど速い
            # ==========================================

            speed = interpolate(
                2.4,
                0.35,
                depth_t
            )

            # ==========================================
            # サイズ
            # ==========================================

            scale = interpolate(
                5.5,
                1.2,
                depth_t
            )

            scale *= np.random.uniform(
                0.7,
                1.4
            )

            # ==========================================
            # 配置
            # ==========================================

            x = np.random.uniform(
                -55,
                35
            )

            y = np.random.uniform(
                -1.5,
                1.6
            )

            cloud = ImageMobject(path)

            cloud.set_resampling_algorithm(
                RESAMPLING_ALGORITHMS["nearest"]
            )

            cloud.scale(scale)

            cloud.move_to(
                np.array([x, y, z])
            )

            cloud.rotate(
                75 * DEGREES,
                axis=RIGHT
            )

            # ==========================================
            # 不透明度
            # ==========================================

            opacity = interpolate(
                0.82,
                0.05,
                depth_t
            )

            opacity *= np.random.uniform(
                0.7,
                1.0
            )

            cloud.set_opacity(opacity)

            # ==========================================
            # 色
            # ==========================================

            darkness = interpolate(
                0.04,
                0.18,
                depth_t
            )

            blue_shift = np.random.uniform(
                0.9,
                1.05
            )

            cloud.set_color(
                rgb_to_color((
                    darkness * 0.7,
                    darkness * 0.8,
                    darkness * blue_shift
                ))
            )

            # ==========================================
            # カスタム属性
            # ==========================================

            cloud.speed = speed
            cloud.depth_t = depth_t

            self.clouds.add(cloud)

        self.add(self.clouds)

        # ==========================================
        # 🌙 海用の月光係数
        # ==========================================

        self.current_moonlight = 1.0

        # ==========================================
        # ☁ 雲アニメーション
        # ==========================================

        def cloud_updater(m, dt):

            moon_x = self.moon_pos[0]

            nearest_dist = 9999.0

            for cloud in self.clouds:

                # 横移動
                cloud.shift(
                    RIGHT * cloud.speed * dt
                )

                # 画面外ループ
                if cloud.get_center()[0] > 12:

                    cloud.shift(
                        LEFT * 26
                    )

                # 月との距離
                dist = abs(
                    cloud.get_center()[0]
                    - moon_x
                )

                nearest_dist = min(
                    nearest_dist,
                    dist
                )

            # ==================================
            # 🌙 海面反射用の減衰
            # ==================================

            fade_radius = 4.0

            if nearest_dist < fade_radius:

                progress = nearest_dist / fade_radius

                self.current_moonlight = interpolate(
                    0.35,
                    1.0,
                    smooth(progress)
                )

            else:

                self.current_moonlight = 1.0

        self.clouds.add_updater(
            cloud_updater
        )



    def construct(self):
        #self.debug()
        music = MusicTimeline(bpm=150, beats_per_bar=4, offset=1.5)
        DEBUG_MODE = False
        # phi: 上下の傾き（俯角）, theta: 左右の回転角
        self.set_camera_orientation(phi=75 * DEGREES, theta=-100 * DEGREES)


        self.set_square()
        self.current_time = 0.0
        self.active_ripples = []

        self.set_moon()
        self.set_cloud()

        if not DEBUG_MODE:
            # 🌊 波＆きらめきパラメータをインスタンス変数にして共通化
            self.WAVE_SPEED = 1.0
            self.WAVE_FREQUENCY = 0.6
            self.WAVE_MIN_BRIGHT = 0.3
            self.SPARKLE_SPEED = 1.0
            self.SPARKLE_INTENSITY = 0.1

            # 1. 海の生成
            sea_dots, self.sea_data_map = self.create_pixel_sea(
                image_path="img/image.png",
                sky_ratio=0.37,
                dot_x=200,
                dot_y=40,
                wave_frequency=self.WAVE_FREQUENCY,
                wave_min_bright=self.WAVE_MIN_BRIGHT,
            )
            sea_group = VGroup(*sea_dots)
            
            self.add(sea_group)
            sea_group.add_updater(lambda g, dt: self.animate_sea_step(g, dt))



        # ========================================================
        # 🎬 メインのタイムライン
        # ========================================================
        time = music.get_duration_by_beats(8)
        longTime = music.get_duration_by_beats(16)

        self.play_lyrics_move(text_string="藁だらけの", speed=0.5)
        self.wait(time)
        self.wait(time)
        self.play_lyrics_move(text_string="海で一人濡れ衣のまま", speed=0.5)
        self.wait(time)
        self.play_lyrics_move(text_string="溺れた", speed=0.5)
        self.wait(time)
        self.play_lyrics_move(text_string="君は語る", speed=0.5)
        self.play_ripple(pos_x=1, pos_y=-4, pos_z=0, max_radius=3.0, expand_speed=0.5)
        self.wait(time)

        self.play_lyrics_move(text_string="首より下の", speed=0.5)
        self.wait(time)
        self.play_lyrics_move(text_string="命を死にゆく誰かに", speed=0.5)
        self.wait(time)
        self.play_lyrics_move(text_string="今すぐ", speed=0.5)
        self.wait(time)
        self.play_lyrics_move(text_string="託したくて", speed=0.5)
        self.wait(time)
        self.play_ripple(pos_x=1, pos_y=-4, pos_z=0, max_radius=3.0, expand_speed=0.5)


        #この後、カメラ位置z座標を+10ぐらいイージングで上げる
        self.move_camera(
            phi=40 * DEGREES,
            theta=-100 * DEGREES,
            run_time=6,
            rate_func=smooth
        )

        self.play_lyrics_move(text_string="待ち続けても何も変わらない", speed=0.5)
        self.wait(time)
        self.play_lyrics_move(text_string="それでも悲劇に期待してる", speed=0.5)
        self.wait(time)
        self.wait(time)
        self.wait(time)
        self.wait(time)


        if not DEBUG_MODE:
            sea_group.clear_updaters()


    def play_ripple(
        self,
        pos_x: float = 0.0,
        pos_y: float = 0.0,
        pos_z: float = 0.0, # 3D配置用ですが水面は基本 Z=0
        max_radius: float = 2.5,
        expand_speed: float = 4.0, # ドット幅に合わせて少し速めがおすすめ
        color: str = "#FFFFFF"     # 今回はドットの輝度にブレンドするため白ベースを推奨
    ):
        """
        水面にドットベースの波紋を展開するため、波紋のパラメータを登録する。
        実際のアニメーション処理は海全体のアップデーター（animate_sea_step）側で行う。
        """
        ripple_info = {
            "center": np.array([pos_x, pos_y, 0.0]), # 水面(Z=0)での中心座標
            "current_radius": 0.01,
            "max_radius": max_radius,
            "expand_speed": expand_speed,
            "color": color
        }
        self.active_ripples.append(ripple_info)


    def animate_sea_step(self, group: VGroup, dt: float):
        """毎フレーム呼び出され、大きな波、きらめき、そしてドット絵の波紋を統合して計算・反映する"""
        self.current_time += dt

        # 1. アクティブな波紋の半径を更新し、寿命が尽きたものは削除する
        alive_ripples = []
        for r in self.active_ripples:
            r["current_radius"] += r["expand_speed"] * dt
            # 最大半径に達していないものだけを残す
            if r["current_radius"] < r["max_radius"]:
                alive_ripples.append(r)
        self.active_ripples = alive_ripples

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

            # 🌊 ① 大きな波のうねり（行単位）
            sin_wave = np.sin(y_local * self.WAVE_FREQUENCY - self.current_time * self.WAVE_SPEED)
            wave_factor = interpolate(current_min_bright, current_max_bright, (sin_wave + 1.0) / 2.0)

            # ✨ ② 個別のきらめき
            sparkle_sin = np.sin(self.current_time * self.SPARKLE_SPEED + sparkle_offset)
            sparkle_factor = 1.0 + (sparkle_sin * self.SPARKLE_INTENSITY)

            total_factor = wave_factor * sparkle_factor

            # ベースとなる海の明度を計算
            new_l = base_l * total_factor
            new_l *= self.current_moonlight
            new_l = min(max(new_l, 0.0), 1.0)
            
            # 🔴 ③ ドット絵波紋のエフェクト重ね合わせ
            # このドットの現在のワールド座標を取得
            rect_pos = rect.get_center()
            
            ripple_bright_bonus = 0.0
            
            for r in self.active_ripples:
                dx = rect_pos[0] - r["center"][0]
                dy = rect_pos[1] - r["center"][1]
                
                # 波紋の中心からこのドットまでの距離を計算 (XとYの平面距離)
                dist = np.sqrt(dx**2 + dy**2)
                current_r = r["current_radius"]

                y_percentage = (rect_pos[1] + 6.0) / 6.0
                y_percentage = min(max(y_percentage, 0.0), 1.0) # 0.0〜1.0に安全ガード

                depth_factor = interpolate(1.2, 0.3, y_percentage)
                depth_factor = min(max(depth_factor, 0.3), 1.2)
                
                # 波紋の線の太さ（ドット絵なので少し肉厚にするのがコツ）
                thickness = 0.25 * depth_factor
                
                # ドットが波紋の輪っかのベロシティ（フチ）の中にいるか
                if abs(dist - current_r) < thickness:
                    # 中心に近いほど、また最大半径に近づくほどフェードアウトさせる
                    progress = current_r / r["max_radius"]
                    fade = 1.0 - progress
                    
                    # 輪っかの中心ほど光が強く、エッジに向かって滑らかになる係数
                    edge_factor = 1.0 - (abs(dist - current_r) / thickness)

                    brightness_mod = edge_factor * fade * 0.5 * depth_factor
                    ripple_bright_bonus += brightness_mod

            # 波紋の光を上乗せ（1.0を超えないように丸める）
            new_l = min(new_l + ripple_bright_bonus, 1.0)

            # 最終的な色を決定して適用
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
                    r, g, b = 2, 2, 5
                
                h, l, s = colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)
                new_l = l * wave_factor
                new_l = new_l * self.current_moonlight
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