from PIL import Image
import numpy as np

W = 256
H = 96

img = np.zeros((H, W, 4), dtype=np.uint8)

# 雲の色
base_color = np.array([140, 170, 210])

# 雲中心
cx = W / 2
cy = H / 2

for y in range(H):
    for x in range(W):

        # 正規化座標
        nx = (x - cx) / (W * 0.5)
        ny = (y - cy) / (H * 0.5)

        # 横長楕円距離
        dist = np.sqrt(nx * nx + (ny * 1.8) ** 2)

        # 雲内部
        if dist < 1.0:

            # 雲輪郭フェード
            fade = (1.0 - dist) ** 1.5

            # ノイズ
            noise = np.random.uniform(0.6, 1.0)

            intensity = fade * noise

            r = int(base_color[0] * intensity)
            g = int(base_color[1] * intensity)
            b = int(base_color[2] * intensity)

            alpha = int(255 * intensity)

            img[y, x] = [r, g, b, alpha]

Image.fromarray(
    img,
    mode="RGBA"
).save("img/cloud_01.png")