from PIL import Image
import numpy as np

W = 256
H = 96

img = np.zeros((H, W, 4), dtype=np.uint8)

base_color = np.array([120, 150, 200])

# ランダムblob
blobs = []

for _ in range(20):

    r = np.random.uniform(20, 60)

    blobs.append({

        "x": np.random.uniform(r, W - r),

        "y": np.random.uniform(r, H - r),

        "r": r
    })

for y in range(H):
    for x in range(W):

        intensity = 0.0

        for b in blobs:

            dx = x - b["x"]
            dy = y - b["y"]

            dist = np.sqrt(dx * dx + dy * dy)

            if dist < b["r"]:

                fade = (1.0 - dist / b["r"]) ** 1.2

                intensity += fade

        intensity *= np.random.uniform(0.5, 0.9)

        intensity = np.clip(intensity, 0.0, 1.0)

        if intensity > 0.02:

            r = int(base_color[0] * intensity)
            g = int(base_color[1] * intensity)
            b = int(base_color[2] * intensity)

            alpha = int(220 * intensity)

            img[y, x] = [r, g, b, alpha]

Image.fromarray(
    img,
    mode="RGBA"
).save("img/cloud_04.png")