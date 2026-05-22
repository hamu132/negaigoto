from PIL import Image
import numpy as np

size = 256

img = np.zeros((size, size, 4), dtype=np.uint8)

center = size / 2

moon_radius = size * 0.1
glow_radius = size * 0.6

for y in range(size):
    for x in range(size):

        dx = x - center
        dy = y - center

        dist = np.sqrt(dx * dx + dy * dy)

        # ==================================
        # 🌙 月本体
        # ==================================

        if dist <= moon_radius:

            v = np.random.randint(170, 235)

            r = np.clip(v - 20, 0, 255)
            g = np.clip(v, 0, 255)
            b = np.clip(v + 10, 0, 255)

            alpha = 255

            img[y, x] = [r, g, b, alpha]

        # ==================================
        # ✨ グロー
        # ==================================

        elif dist <= glow_radius:

            t = (
                (dist - moon_radius)
                / (glow_radius - moon_radius)
            )

            glow = (1.0 - t) ** 2

            # ノイズ追加
            noise = np.random.uniform(0.7, 1.0)

            intensity = glow * noise

            r = int(180 * intensity)
            g = int(220 * intensity)
            b = int(255 * intensity)

            alpha = int(120 * intensity)

            img[y, x] = [r, g, b, alpha]

Image.fromarray(
    img,
    mode="RGBA"
).save("img/moon_with_glow.png")