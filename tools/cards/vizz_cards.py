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


def showcase(path, tname, eyebrow, head, coral_last=None, shot=None, crop=None,
             caption="Sample report for a made-up brand", head_size=66):
    """Headline at the top, a real report page (or slide) below it in a frame.
    shot: image path; crop: (x0, y0, x1, y1) as fractions of the shot."""
    bg, fg = theme(tname)
    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)
    tracked(d, (M, 128), eyebrow, font("700", 25), CORAL, 6.5)
    fh = font("700", head_size)
    lh = int(head_size * 1.2)
    check_width(d, head + ([coral_last] if coral_last else []), fh)
    y = 196
    for ln in head:
        d.text((M, y), ln, font=fh, fill=fg)
        y += lh
    if coral_last:
        d.text((M, y), coral_last, font=fh, fill=CORAL)
        y += lh
    top = y + 40
    cap_h = 52
    bottom = 1180 - cap_h
    if isinstance(shot, (list, tuple)):
        _stack(img, d, bg, fg, shot, top, bottom, caption)
        footer(d, bg, fg)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        img.save(path, "JPEG", quality=95)
        print("wrote", os.path.basename(path))
        return
    sh = Image.open(shot).convert("RGB")
    if crop:
        x0, y0, x1, y1 = crop
        sh = sh.crop((int(x0 * sh.width), int(y0 * sh.height), int(x1 * sh.width), int(y1 * sh.height)))
    box_w, box_h = W - 2 * M, bottom - top
    s = min(box_w / sh.width, box_h / sh.height)
    sh = sh.resize((int(sh.width * s), int(sh.height * s)), Image.LANCZOS)
    x = (W - sh.width) // 2
    # soft shadow, then a thin frame
    shadow = Image.new("RGB", (sh.width + 24, sh.height + 24), bg)
    sd = ImageDraw.Draw(shadow)
    sd.rectangle([(12, 16), (sh.width + 12, sh.height + 16)], fill=mix(bg, (0, 0, 0), 0.35))
    from PIL import ImageFilter
    shadow = shadow.filter(ImageFilter.GaussianBlur(9))
    img.paste(shadow, (x - 12, top - 12))
    img.paste(sh, (x, top))
    d.rectangle([(x - 1, top - 1), (x + sh.width, top + sh.height)], outline=mix(bg, fg, 0.25), width=2)
    if caption:
        fcap = font("600", 26)
        d.text((x, top + sh.height + 18), caption, font=fcap, fill=mix(bg, fg, 0.55))
    footer(d, bg, fg)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, "JPEG", quality=95)
    print("wrote", os.path.basename(path))


def _frame(img, d, bg, fg, sh, x, y):
    from PIL import ImageFilter
    shadow = Image.new("RGB", (sh.width + 40, sh.height + 40), bg)
    ImageDraw.Draw(shadow).rectangle([(20, 26), (sh.width + 20, sh.height + 26)], fill=mix(bg, (0, 0, 0), 0.4))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    img.paste(shadow, (x - 20, y - 20))
    img.paste(sh, (x, y))
    d.rectangle([(x - 1, y - 1), (x + sh.width, y + sh.height)], outline=mix(bg, fg, 0.25), width=2)


def _stack(img, d, bg, fg, shots, top, bottom, caption):
    """Two landscape slides, the second overlapping lower right, like a deck."""
    a, b = [Image.open(s).convert("RGB") for s in shots]
    box_w, box_h = W - 2 * M, bottom - top
    sw = int(box_w * 0.86)
    sh_h = int(sw * a.height / a.width)
    dy = box_h - sh_h
    if dy < sh_h * 0.45:  # keep at least half of slide 1 visible
        sh_h = int(box_h / 1.45); sw = int(sh_h * a.width / a.height); dy = box_h - sh_h
    a = a.resize((sw, sh_h), Image.LANCZOS); b = b.resize((sw, sh_h), Image.LANCZOS)
    _frame(img, d, bg, fg, a, M, top)
    _frame(img, d, bg, fg, b, W - M - sw, top + dy)
    if caption:
        d.text((M, top + box_h + 18), caption, font=font("600", 26), fill=mix(bg, fg, 0.55))
