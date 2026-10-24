# GUIDA-SVILUPPO: genera il LOGO (montagna innevata) coi colori di _data/tema.json (campo "accent").
# Uso, dalla radice del sito:  python automation/genera_logo.py        (oppure: python automation/genera_logo.py "#0b6cf0")
# Scrive: assets/images/favicon.svg, favicon-32/192/512.png, apple-touch-icon.png, favicon.ico (in assets/images e nella radice).
# Va rilanciato dopo ogni cambio di accento (nuovo_sito.ps1 -Accento scrive tema.json: poi lancia questo). Richiede Pillow.
import json, os, sys
from PIL import Image, ImageDraw
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, 'assets', 'images')
def hx(s): s = s.lstrip('#'); return tuple(int(s[i:i+2], 16) for i in (0, 2, 4))
def mix(a, b, t): return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))
def h(c): return '#%02x%02x%02x' % c
acc = sys.argv[1] if len(sys.argv) > 1 else json.load(open(os.path.join(ROOT, '_data', 'tema.json'), encoding='utf-8')).get('accent', '#0e7490')
A = hx(acc); W = (255, 255, 255); K = (0, 0, 0)
C = dict(top=mix(A, W, .80), bot=mix(A, W, .50), back=mix(A, W, .55), rock=mix(A, K, .45), shade=mix(mix(A, K, .45), K, .35), snow=W, snowsh=mix(A, W, .85))  # cielo celestino chiaro, montagna scura

P = dict(
  back=[(44,24),(68,64),(20,64)], backcap=[(44,24),(48.6,31.7),(45.6,30.4),(43,33),(40.4,30.6)],
  rock=[(27,10),(58,64),(-4,64)], shade=[(27,10),(58,64),(33,64),(29,33)],
  cap=[(27,10),(36.3,26.4),(31.8,30.4),(27.6,25.6),(23.2,30.4),(17.7,26.4)], capsh=[(27,10),(36.3,26.4),(31.8,30.4),(28.6,26.6)])
def pts(l): return ' '.join('%g,%g' % p for p in l)
svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs><linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient><clipPath id="c"><rect width="64" height="64" rx="14"/></clipPath></defs><rect width="64" height="64" rx="14" fill="url(#s)"/><g clip-path="url(#c)">'
  '<polygon points="%s" fill="%s"/><polygon points="%s" fill="%s"/><polygon points="%s" fill="%s" opacity=".35"/><polygon points="%s" fill="#fff"/><polygon points="%s" fill="%s"/></g></svg>\n'
  % (h(C['top']), h(C['bot']), pts(P['back']), h(C['back']), pts(P['rock']), h(C['rock']), pts(P['shade']), '#000', pts(P['cap']), pts(P['capsh']), h(C['snowsh'])))
open(os.path.join(IMG, 'favicon.svg'), 'w', encoding='utf-8', newline='\n').write(svg)
def render(N, round_=True):
    S = N * 4; k = S / 64
    im = Image.new('RGB', (S, S)); d = ImageDraw.Draw(im)
    for y in range(S): d.line([(0, y), (S, y)], fill=mix(C['top'], C['bot'], y / (S - 1)))
    def poly(l, c): d.polygon([(x * k, y * k) for x, y in l], fill=c)
    poly(P['back'], C['back']); poly(P['rock'], C['rock']); poly(P['shade'], C['shade']); poly(P['cap'], W); poly(P['capsh'], C['snowsh'])
    im = im.resize((N, N), Image.LANCZOS).convert('RGBA')
    if round_:
        m = Image.new('L', (S, S), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, S - 1, S - 1], radius=14 * k, fill=255)
        im.putalpha(m.resize((N, N), Image.LANCZOS))
    return im
for n in (512, 192, 32): render(n).save(os.path.join(IMG, 'favicon-%d.png' % n))
render(180, False).convert('RGB').save(os.path.join(IMG, 'apple-touch-icon.png'))
ico = render(256)
for p in (os.path.join(IMG, 'favicon.ico'), os.path.join(ROOT, 'favicon.ico')): ico.save(p, sizes=[(16,16),(32,32),(48,48),(64,64)])
print('logo generato con accento', acc)