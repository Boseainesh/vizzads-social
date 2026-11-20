"""Vizz Ads card builder (launch-pack style). 1080x1350 JPEG.
Rebuilt 20 Nov from the week-1 builder (project doc claude/social-creative-builder-week1.py)."""
import os
from PIL import Image, ImageDraw, ImageFont

NAVY, CREAM, CORAL = (11, 19, 43), (243, 240, 221), (225, 120, 91)
W, H, M = 1080, 1350, 96
FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
WEIGHT = {"600": "SemiBold", "700": "Bold", "400": "Regular"}


def font(w, s):
    return ImageFont.truetype(os.path.join(FONTS, "Outfit-%s.ttf" % WEIGHT[w]), s)


def mix(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def tracked(d, xy, text, fnt, fill, trk=0):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=fnt, fill=fill)
        x += d.textlength(ch, font=fnt) + trk


def theme(name):
    return (NAVY, CREAM) if name == "navy" else (CREAM, NAVY)


def footer(d, bg, fg):
    fy = 1216
    d.rectangle([(M, fy), (W - M, fy + 2)], fill=mix(bg, fg, 0.20))
    f = font("700", 34)
    by = fy + 44
    d.text((M, by), "Vizz", font=f, fill=CORAL)
    d.text((M + d.textlength("Vizz", font=f), by), "Ads", font=f, fill=fg)
    u = "vizzads.com"
    d.text((W - M - d.textlength(u, font=f), by), u, font=f, fill=CORAL)


def check_width(d, lines, fnt):
    for ln in lines:
        assert d.textlength(ln, font=fnt) <= W - 2 * M, "too wide: " + ln


def card(path, tname, eyebrow, head, coral_last=None, body=None, closing=None,
         head_size=78, items=None, number=None):
    """head: list of lines (navy/cream); coral_last: final headline line in coral."""
    bg, fg = theme(tname)
    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)
    tracked(d, (M, 128), eyebrow, font("700", 25), CORAL, 6.5)
    if number:
        fnum = font("700", 25)
        tracked(d, (W - M - d.textlength(number, font=fnum) - 10, 128), number, fnum,
                mix(bg, fg, 0.45), 4)

    fh = font("700", head_size)
    lh = int(head_size * 1.2)
    check_width(d, head + ([coral_last] if coral_last else []), fh)
    y = 208
    for ln in head:
        d.text((M, y), ln, font=fh, fill=fg)
        y += lh
    if coral_last:
        d.text((M, y), coral_last, font=fh, fill=CORAL)
        y += lh

    ry = y + 52
    d.rectangle([(M, ry), (W - M, ry + 2)], fill=mix(bg, fg, 0.20))
    y = ry + 62

    if items:
        fn, fi = font("700", 23), font("600", 44)
        check_width(d, [" " * 6 + i for i in items], fi)
        for i, label in enumerate(items, 1):
            tracked(d, (M, y + 14), "%02d" % i, fn, CORAL, 3.0)
            d.text((M + 88, y), label, font=fi, fill=fg)
            y += 96
        y += 20

    if body:
        fb = font("600", 41)
        check_width(d, body, fb)
        for ln in body:
            d.text((M, y), ln, font=fb, fill=fg)
            y += 57
        y += 40

    if closing:
        fc = font("700", 43)
        check_width(d, closing, fc)
        cy = max(y, 1150 - 54 * len(closing))
        for ln in closing:
            d.text((M, cy), ln, font=fc, fill=CORAL)
            cy += 54
        assert cy <= 1200, "closing overruns footer: " + path

    assert y <= 1200, "body overruns footer: " + path
    footer(d, bg, fg)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.convert("RGB").save(path, "JPEG", quality=95)  # JPEG: Meta's API needs it
    print("wrote", os.path.basename(path))
