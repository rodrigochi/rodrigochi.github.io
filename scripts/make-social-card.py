"""Render assets/social-card.png (1200x630) with the site palette and fonts.
Fonts: Newsreader, Schibsted Grotesk, IBM Plex Mono (Google Fonts TTFs) in FONT_DIR."""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'scripts', 'fonts')
S = 2; W, H = 1200 * S, 630 * S
PAPER = (242, 245, 247); INK = (21, 33, 43); INK2 = (58, 73, 87); MUTED = (94, 109, 122); RULE = (212, 220, 226); TEAL = (15, 123, 132)

def font(name, size, axes=None):
    f = ImageFont.truetype(os.path.join(FONT_DIR, name), size * S)
    if axes: f.set_variation_by_axes(axes)
    return f

im = Image.new('RGB', (W, H), PAPER); d = ImageDraw.Draw(im)
name = font('Newsreader.ttf', 68, [400, 72])          # axes: weight, optical size
sub = font('Schibsted.ttf', 27, [450]); small = font('Schibsted.ttf', 22, [400]); mono = font('PlexMono.ttf', 17)
P = 72 * S
d.ellipse([P, P + 4 * S, P + 10 * S, P + 14 * S], fill=TEAL)
d.text((P + 22 * S, P - 2 * S), 'SEISMOLOGY  ·  GEOMAGNETISM  ·  CTBTO', font=mono, fill=TEAL)
av = Image.open(os.path.join(ROOT, 'assets/avatar.jpg')).convert('RGB').resize((230 * S, 230 * S), Image.LANCZOS)
m = Image.new('L', av.size, 0); ImageDraw.Draw(m).ellipse([0, 0, av.size[0] - 1, av.size[1] - 1], fill=255)
py = 128 * S; im.paste(av, (P, py), m)
x = P + 230 * S + 56 * S
d.text((x, py + 22 * S), 'Rodrigo Chi Durán', font=name, fill=INK)
d.text((x, py + 118 * S), 'Seismic-Acoustic Officer · CTBTO, Vienna', font=sub, fill=INK2)
d.text((x, py + 164 * S), 'Seismic sources · explosion monitoring · Earth’s core', font=small, fill=MUTED)
tr = json.load(open(os.path.join(ROOT, 'assets/mdj_2017-09-03_BHZ.json'))); y = tr['y']; n = len(y)
top, bot = 412 * S, 530 * S; mid = (top + bot) / 2; amp = (bot - top) / 2 * 0.95; x0, x1 = P, W - P
pts = [(x0 + (x1 - x0) * i / (n - 1), mid - (abs(v) ** 0.55 * (1 if v >= 0 else -1)) * amp) for i, v in enumerate(y)]
d.line(pts, fill=INK, width=max(1, int(1.1 * S)), joint='curve')
px = x0 + (x1 - x0) * tr['pick'] / tr['dur']
for yy in range(int(top - 10 * S), int(bot), 9 * S): d.line([(px, yy), (px, yy + 4 * S)], fill=TEAL, width=2 * S)
d.text((px + 8 * S, top - 14 * S), 'P', font=mono, fill=TEAL)
d.line([(P, 562 * S), (W - P, 562 * S)], fill=RULE, width=S)
d.text((P, 576 * S), 'IC.MDJ · 2017-09-03 DPRK test, P picked by STA/LTA', font=mono, fill=MUTED)
url = 'rodrigochi.github.io'; d.text((W - P - d.textlength(url, font=small), 572 * S), url, font=small, fill=TEAL)
im.resize((1200, 630), Image.LANCZOS).save(os.path.join(ROOT, 'assets/social-card.png'), optimize=True)
print('assets/social-card.png written')
