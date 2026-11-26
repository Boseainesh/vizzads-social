"""Vizz Ads card builder (green & pink brand colours, 26 Nov 2026) (launch-pack style). 1080x1350 JPEG.
Rebuilt 20 Nov from the week-1 builder (project doc claude/social-creative-builder-week1.py)."""
import os
from PIL import Image, ImageDraw, ImageFont

# Brand colours (agreed 26 Nov 2026). Use nothing else.
FOREST, CARD, SAGE = (24, 41, 33), (36, 68, 55), (78, 115, 99)
OFFWHITE, DAYTINT, WHITE = (243, 246, 243), (232, 239, 235), (255, 255, 255)
PINK, DEEPPINK = (255, 143, 191), (194, 24, 91)
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


def palette(name):
    """'navy' (and 'dark') = dark theme; 'cream' (and 'light') = light theme."""
    if name in ("navy", "dark"):
        return dict(dark=True, bg=FOREST, fg=OFFWHITE, accent=PINK, closing=PINK,
                    muted=mix(FOREST, OFFWHITE, 0.70), line=CARD, frame=CARD,
                    url=PINK, pill_text=PINK, pill_fill=mix(FOREST, PINK, 0.16))
    return dict(dark=False, bg=OFFWHITE, fg=FOREST, accent=FOREST, closing=FOREST,
                muted=SAGE, line=DAYTINT, frame=SAGE,
                url=FOREST, pill_text=FOREST, pill_fill=mix(OFFWHITE, PINK, 0.18))


def theme(name):
    p = palette(name)
    return p["bg"], p["fg"]


def background(name, gradient=False):
    """Plain background, or Card Green -> Forest Green for dark hero/offer posts."""
    p = palette(name)
    img = Image.new("RGB", (W, H), p["bg"])
    if gradient and p["dark"]:
        d = ImageDraw.Draw(img)
        for yy in range(H):
            d.line([(0, yy), (W, yy)], fill=mix(CARD, FOREST, yy / (H - 1)))
    return img


def pill(d, x, y, text, name):
    """ALL CAPS label: pink-tint pill, Vizz Pink border, pink dot."""
    p = palette(name)
    f = font("700", 25)
    tw = sum(d.textlength(ch, font=f) + 5.0 for ch in text) - 5.0
    h, padx, dot = 50, 24, 10
    w = padx + dot + 14 + tw + padx
    d.rounded_rectangle([(x, y), (x + w, y + h)], radius=h // 2, fill=p["pill_fill"], outline=PINK, width=2)
    cx, cy = x + padx + dot // 2, y + h // 2
    d.ellipse([(cx - dot // 2, cy - dot // 2), (cx + dot // 2, cy + dot // 2)], fill=PINK)
    tracked(d, (x + padx + dot + 14, y + 11), text, f, p["pill_text"], 5.0)


def highlight(d, xy, text, fnt, name):
    """Key headline line: Vizz Pink on dark; Forest Green + pink stripe on light."""
    p = palette(name)
    x, y = xy
    if not p["dark"]:
        l, t, r, b = d.textbbox((x, y), text, font=fnt)
        mid = t + (b - t) * 0.52
        d.rectangle([(l - 6, mid), (r + 6, b + 4)], fill=PINK)
    d.text((x, y), text, font=fnt, fill=p["accent"])


def footer(d, name):
    p = palette(name)
    fy = 1216
    d.rectangle([(M, fy), (W - M, fy + 2)], fill=p["line"])
    f = font("700", 34)
    by = fy + 44
    d.text((M, by), "Vizz", font=f, fill=DEEPPINK)
    d.text((M + d.textlength("Vizz", font=f) + 1, by), "Ads", font=f, fill=p["fg"])
    u = "vizzads.com"
    d.text((W - M - d.textlength(u, font=f), by), u, font=f, fill=p["url"])


def check_width(d, lines, fnt):
    for ln in lines:
        assert d.textlength(ln, font=fnt) <= W - 2 * M, "too wide: " + ln


def card(path, tname, eyebrow, head, coral_last=None, body=None, closing=None,
         head_size=78, items=None, number=None, gradient=False):
    """head: lines in the main text colour; coral_last: the highlighted last line
    (Vizz Pink on dark, Forest Green + pink stripe on light). gradient: dark hero/offer posts."""
    p = palette(tname)
    img = background(tname, gradient)
    d = ImageDraw.Draw(img)
    pill(d, M, 116, eyebrow, tname)
    if number:
        fnum = font("700", 25)
        tracked(d, (W - M - d.textlength(number, font=fnum) - 10, 128), number, fnum, p["muted"], 4)

    fh = font("700", head_size)
    lh = int(head_size * 1.2)
    check_width(d, head + ([coral_last] if coral_last else []), fh)
    y = 208
    for ln in head:
        d.text((M, y), ln, font=fh, fill=p["fg"])
        y += lh
    if coral_last:
        highlight(d, (M, y), coral_last, fh, tname)
        y += lh

    ry = y + 52
    d.rectangle([(M, ry), (W - M, ry + 2)], fill=p["line"])
    y = ry + 62

    if items:
        fn, fi = font("700", 23), font("600", 44)
        check_width(d, [" " * 6 + i for i in items], fi)
        for i, label in enumerate(items, 1):
            num = "%02d" % i
            if p["dark"]:
                tracked(d, (M, y + 14), num, fn, PINK, 3.0)
            else:
                cx, cy, r = M + 24, y + 29, 27
                d.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=PINK)
                tw = d.textlength(num, font=fn) + 3.0
                tracked(d, (cx - tw / 2, cy - 15), num, fn, FOREST, 3.0)
            d.text((M + 88, y), label, font=fi, fill=p["fg"])
            y += 96
        y += 20

    if body:
        fb = font("600", 41)
        check_width(d, body, fb)
        for ln in body:
            d.text((M, y), ln, font=fb, fill=p["fg"])
            y += 57
        y += 40

    if closing:
        fc = font("700", 43)
        check_width(d, closing, fc)
        cy = max(y, 1150 - 54 * len(closing))
        for ln in closing:
            d.text((M, cy), ln, font=fc, fill=p["closing"])
            cy += 54
        assert cy <= 1200, "closing overruns footer: " + path

    assert y <= 1200, "body overruns footer: " + path
    footer(d, tname)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.convert("RGB").save(path, "JPEG", quality=95)  # JPEG: Meta's API needs it
    print("wrote", os.path.basename(path))


def showcase(path, tname, eyebrow, head, coral_last=None, shot=None, crop=None,
             caption="Sample report for a made-up brand", head_size=66, gradient=False):
    """Headline at the top, a real report page (or slide) below it in a frame.
    shot: image path; crop: (x0, y0, x1, y1) as fractions of the shot."""
    p = palette(tname)
    bg, fg = p["bg"], p["fg"]
    img = background(tname, gradient)
    d = ImageDraw.Draw(img)
    pill(d, M, 116, eyebrow, tname)
    fh = font("700", head_size)
    lh = int(head_size * 1.2)
    check_width(d, head + ([coral_last] if coral_last else []), fh)
    y = 196
    for ln in head:
        d.text((M, y), ln, font=fh, fill=fg)
        y += lh
    if coral_last:
        highlight(d, (M, y), coral_last, fh, tname)
        y += lh
    top = y + 40
    cap_h = 52
    bottom = 1180 - cap_h
    if isinstance(shot, (list, tuple)):
        _stack(img, d, tname, shot, top, bottom, caption)
        footer(d, tname)
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
    d.rectangle([(x - 1, top - 1), (x + sh.width, top + sh.height)], outline=p["frame"], width=2)
    if caption:
        fcap = font("600", 26)
        d.text((x, top + sh.height + 18), caption, font=fcap, fill=p["muted"])
    footer(d, tname)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, "JPEG", quality=95)
    print("wrote", os.path.basename(path))


def _frame(img, d, tname, sh, x, y):
    p = palette(tname)
    bg = p["bg"]
    from PIL import ImageFilter
    shadow = Image.new("RGB", (sh.width + 40, sh.height + 40), bg)
    ImageDraw.Draw(shadow).rectangle([(20, 26), (sh.width + 20, sh.height + 26)], fill=mix(bg, (0, 0, 0), 0.4))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    img.paste(shadow, (x - 20, y - 20))
    img.paste(sh, (x, y))
    d.rectangle([(x - 1, y - 1), (x + sh.width, y + sh.height)], outline=p["frame"], width=2)


def _stack(img, d, tname, shots, top, bottom, caption):
    """Two landscape slides, the second overlapping lower right, like a deck."""
    a, b = [Image.open(s).convert("RGB") for s in shots]
    box_w, box_h = W - 2 * M, bottom - top
    sw = int(box_w * 0.86)
    sh_h = int(sw * a.height / a.width)
    dy = box_h - sh_h
    if dy < sh_h * 0.45:  # keep at least half of slide 1 visible
        sh_h = int(box_h / 1.45); sw = int(sh_h * a.width / a.height); dy = box_h - sh_h
    a = a.resize((sw, sh_h), Image.LANCZOS); b = b.resize((sw, sh_h), Image.LANCZOS)
    _frame(img, d, tname, a, M, top)
    _frame(img, d, tname, b, W - M - sw, top + dy)
    if caption:
        d.text((M, top + box_h + 18), caption, font=font("600", 26), fill=palette(tname)["muted"])
