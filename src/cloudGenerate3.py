from PIL import Image
import numpy as np

W = 256
H = 128

img = np.zeros((H, W, 4), dtype=np.uint8)

base_color = np.array([120, 145, 185])

cx = W / 2
cy = H / 2

for y in range(H):
    for x in range(W):

        nx = (x - cx) / (W * 0.5)
        ny = (y - cy) / (H * 0.5)

        dist = np.sqrt(
            (nx * 0.9) ** 2
            + (ny * 1.5) ** 2
        )

        if dist < 1.0:

            fade = (1.0 - dist) ** 0.5

            # 大きめノイズ
            noise = (
                np.sin(x * 0.08)
                * np.sin(y * 0.12)
            )

            noise = (
                (noise + 1.0)
                * 0.5
            )

            rand = np.random.uniform(
                0.75,
                1.0
            )

            intensity = (
                fade
                * noise
                * rand
            )

            intensity = np.clip(
                intensity,
                0.0,
                1.0
            )

            r = int(base_color[0] * intensity)
            g = int(base_color[1] * intensity)
            b = int(base_color[2] * intensity)

            alpha = int(255 * intensity)

            img[y, x] = [r, g, b, alpha]

Image.fromarray(
    img,
    mode="RGBA"
).save("img/cloud_03.png")