# negaigoto

プロジェクトの説明をここに記載します。
# 高画質モード（プレビューなし）
manim -qh src/main.py MoveSquare

# 低画質テストモード（プレビューなし）
manim -ql src/main.py MoveSquare


# カラーコードで色を指定
cube = Cube(side_length=2, fill_color="#1a237e", fill_opacity=0.8)

# 2. カメラの初期角度（視点）を設定する
# phi: 上下の傾き（俯角）, theta: 左右の回転角
self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

# 登場
self.add(square)
# アニメーション
self.play(square.animate...)

# 複数の物体を一度に
self.play(*[FadeIn(c) for c in cubes])


# 図形
Cube//立方体
Square//
Rectangle//

cyber_box = Rectangle(
    width=4.0, 
    height=1.5, 
    stroke_color="#00ffff", # 鮮やかなシアン
    stroke_width=3,         # 枠線をちょっと太く
    fill_opacity=0.0        # 中身はスケスケ
)