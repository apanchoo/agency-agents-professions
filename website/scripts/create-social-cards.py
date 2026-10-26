"""Render the site's own vector mark and typography into social PNG cards.

Run with Python and Pillow. These static assets do not add a website dependency.
"""
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont

SITE = Path(__file__).resolve().parents[1]
catalog = json.loads((SITE.parent / 'extensions/professions/catalog.json').read_text(encoding='utf-8'))
PROFESSIONS = len(catalog)
TOTAL = PROFESSIONS + 283
SCALE = 3


def font(size, bold=False):
    candidates = [Path('C:/Windows/Fonts') / ('segoeuib.ttf' if bold else 'segoeui.ttf'),
      Path('/usr/share/fonts/truetype/dejavu') / ('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')]
    for candidate in candidates:
        if candidate.exists(): return ImageFont.truetype(str(candidate), round(size * SCALE))
    raise RuntimeError('Install Segoe UI or DejaVu Sans to reproduce the social cards.')


def card(filename, width, height, dark):
    sx, sy = width / 1200, height / 630
    bg, ink, muted, accent, line = (('#172c28', '#f4f3ec', '#d5dfd1', '#c7f275', '#486053') if dark else
                                  ('#f4f3ec', '#172c28', '#43534a', '#245b43', '#ccd2c7'))
    im = Image.new('RGB', (width * SCALE, height * SCALE), bg)
    draw = ImageDraw.Draw(im)
    def xy(x, y): return (round(x * sx * SCALE), round(y * sy * SCALE))
    def text(x, y, value, size, color=ink, bold=False):
        draw.text(xy(x, y), value, font=font(size * sy, bold), fill=color, anchor='lt')
    def rule(points, color, thickness=2): draw.line([xy(*p) for p in points], fill=color, width=round(thickness * SCALE), joint='curve')
    def logo(x, y, size):
        # Same two polygons and rounded square as static/img/mark.svg.
        draw.rounded_rectangle([xy(x,y), xy(x+size,y+size)], radius=round(size/5*SCALE), fill='#172c28', outline=line, width=2*SCALE)
        for points, color in [([(9,29),(18,10),(23,10),(31,29),(25,29),(23,24),(15,24),(13,29)], '#c7f275'),
                              ([(17,19),(21,19),(19,14)], '#172c28')]:
            draw.polygon([xy(x+px*size/40,y+py*size/40) for px,py in points], fill=color)
    logo(64, 48, 72)
    text(158, 54, 'AGENCY / PROFESSIONS', 25, ink, True)
    text(158, 91, 'THE PROFESSIONAL AI AGENT LIBRARY', 18, accent, True)
    text(59, 160, 'AI expertise.', 88, ink, True)
    text(59, 264, 'Ready to work.', 88, accent, True)
    # A quiet vector arrow echoes the site's specimen and action icons.
    rule([(960,312),(1090,182)], line, 12)
    rule([(970,182),(1090,182),(1090,302)], line, 12)
    text(65, 376, 'Open-source agents. Practical skills. Real professions.', 25, muted)
    rule([(64,438),(1136,438)], line, 2)
    text(64, 470, f'{TOTAL:,}', 43, ink, True)
    text(64, 523, 'AI agents to explore', 21, muted)
    text(425, 470, f'{PROFESSIONS:,}', 43, ink, True)
    text(425, 523, 'companion skills', 21, muted)
    text(780, 478, 'Built from France Travail', 23, accent, True)
    text(780, 515, 'Occupational open data', 20, muted)
    text(64, 584, 'apanchoo.github.io/agency-agents-professions', 18, muted)
    output = SITE / 'static/img' / filename
    im.resize((width,height),Image.Resampling.LANCZOS).save(output, optimize=True)
    assert output.stat().st_size < 1_000_000
    print(filename, f'{width}x{height}', output.stat().st_size, 'bytes')


if __name__ == '__main__':
    card('social-site.png', 1200, 630, False)
    card('social-repository.png', 1280, 640, True)
