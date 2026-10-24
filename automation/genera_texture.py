# GUIDA-SVILUPPO: genera lo sfondo della home (assets/images/leather-hero.jpg): pelle grana fine + cucitura a punti.
# Uso, dalla radice del sito:  python automation/genera_texture.py   (colori da _data/tema.json). Richiede Pillow + numpy.
import json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1920, 1080
tema = json.load(open(os.path.join(ROOT, '_data', 'tema.json'), encoding='utf-8'))
def hx(s): s = s.lstrip('#'); return np.array([int(s[i:i+2], 16) for i in (0, 2, 4)], float)
base = hx(tema.get('accent', '#8a6a3a')) * .55 + hx('#f3e7d3') * .45
rng = np.random.default_rng(7)
def noise(scale, amp):
    n = rng.normal(0, 1, (H // scale + 2, W // scale + 2)).astype('float32')
    im = Image.fromarray(((n - n.min()) / (n.max() - n.min()) * 255).astype('uint8')).resize((W, H), Image.BICUBIC)
    return (np.asarray(im, 'float32') / 255 - .5) * amp
grain = noise(2, 26) + noise(5, 20) + noise(14, 14) + noise(60, 22)
# venature a "cellule" della pelle: bordi di una griglia di punti casuali
pts = rng.random((420, 2)) * (W, H)
yy, xx = np.mgrid[0:H:3, 0:W:3]
d = np.full(yy.shape, 1e9, 'float32'); d2 = d.copy()
for px, py in pts:
    dist = np.hypot(xx - px, yy - py)
    d2 = np.minimum(d2, np.maximum(d, dist)); d = np.minimum(d, dist)
cell = np.clip((d2 - d) / 14, 0, 1)
cell = np.asarray(Image.fromarray((cell * 255).astype('uint8')).resize((W, H), Image.BICUBIC), 'float32') / 255
img = base[None, None, :] + grain[..., None] * .9 - (1 - cell)[..., None] * 16
vy, vx = np.mgrid[0:H, 0:W]
vig = 1 - .28 * (((vx - W / 2) / (W / 2)) ** 2 + ((vy - H / 2) / (H / 2)) ** 2) ** .9
img = np.clip(img * vig[..., None], 0, 255).astype('uint8')
im = Image.fromarray(img).filter(ImageFilter.GaussianBlur(.6))
# cucitura a punti lungo il bordo
dr = ImageDraw.Draw(im, 'RGBA'); m = 46
thread = (244, 233, 212, 235); shade = (60, 38, 24, 90)
for (x0, y0, x1, y1) in ((m, m, W - m, m), (m, H - m, W - m, H - m), (m, m, m, H - m), (W - m, m, W - m, H - m)):
    L = int(np.hypot(x1 - x0, y1 - y0)); st = 26
    for i in range(0, L - st, st + 14):
        a = i / L; b = (i + st) / L
        ax, ay = x0 + (x1 - x0) * a, y0 + (y1 - y0) * a; bx, by = x0 + (x1 - x0) * b, y0 + (y1 - y0) * b
        dr.line((ax + 1.5, ay + 2, bx + 1.5, by + 2), fill=shade, width=5)
        dr.line((ax, ay, bx, by), fill=thread, width=4)
im.save(os.path.join(ROOT, 'assets', 'images', 'leather-hero.jpg'), quality=82, optimize=True, progressive=True)
print('ok leather-hero.jpg')
