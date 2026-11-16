"""Cover 1920x1080 from episode.COVER = dict(lines=[(text, (r,g,b)), ...], layers=[(asset, cx_px, bottom_px, height_px), ...], text_x=1180)"""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import render
from episode import COVER
W, H = 1920, 1080
c = render.Canvas(render.flat_bg(render.FLAT)); c.im = c.im.convert('RGBA')
for (n, x, by, h) in COVER['layers']:
    render.place(c, n, x, by, h, shadow=not n.startswith('C09'))
im = c.im; tx = COVER.get('text_x', 1180)
lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
y = 250
for i, (txt, col) in enumerate(COVER['lines']):
    size = 190 if i == 0 else 150
    f = ImageFont.truetype(os.path.join(render.HERE, 'fonts', 'Kanit-Bold.ttf'), size, layout_engine=ImageFont.Layout.RAQM)
    ds.text((tx + 8, y + 10), txt, font=f, fill=(0, 20, 30, 200), anchor='mm')
    d.text((tx, y), txt, font=f, fill=tuple(col) + (255,), anchor='mm', stroke_width=6, stroke_fill=(20, 40, 50))
    y += 200
sh = sh.filter(ImageFilter.GaussianBlur(8)); im.alpha_composite(sh); im.alpha_composite(lay)
im.convert('RGB').save(sys.argv[1], quality=90); print('cover ->', sys.argv[1])
