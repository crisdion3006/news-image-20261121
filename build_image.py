#!/usr/bin/env python3
"""Front page for Saturday 21 November 2026 (make.fun news-image-20261121).

Draws one 1024x1024 PNG with PIL: a burgundy masthead, the date, a Kryvyi
Rih hero over a drawn night skyline, four story cards and an also-today
strip. Every word is rendered text; every picture is flat shapes. No
network, no generated text, no copied art.

Stories (verified 21 Nov 2026): Russian double-tap strike on Kryvyi Rih
(kills a 7-year-old boy and a 20-year-old paramedic, 42 injured); COP31
spills into overtime in Antalya; ICJ finds Myanmar committed genocide
against the Rohingya; Cyclone Akvan weakens over Odisha; JPMorgan, Visa
and Mastercard confirm third-party vendor breaches.
"""

import math
import random

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
MARGIN = 28

PAL = {
    "paper": (247, 243, 232),
    "ink": (26, 26, 26),
    "white": (255, 255, 255),
    "red": (178, 28, 28),
    "wine": (112, 20, 28),
    "gold": (201, 162, 39),
    "edge": (201, 194, 172),
    "body": (58, 54, 46),
    "strip": (232, 226, 208),
    "sand": (228, 196, 150),
}

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load(kind, size):
    names = {
        "serif": "DejaVuSerif-Bold.ttf",
        "bold": "DejaVuSans-Bold.ttf",
        "plain": "DejaVuSans.ttf",
    }
    return ImageFont.truetype(f"{FONT_DIR}/{names[kind]}", size)


def flow(pen, text, face, width):
    """Split text into lines that fit width (greedy word wrap)."""
    out, cur = [], ""
    for word in text.split(" "):
        nxt = f"{cur} {word}".strip()
        if pen.textlength(nxt, font=face) <= width:
            cur = nxt
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def centred(pen, y, text, face, fill, canvas_w=SIZE):
    w = pen.textlength(text, font=face)
    pen.text(((canvas_w - w) / 2, y), text, font=face, fill=fill)


def starburst(pen, cx, cy, radius, fill):
    pts = []
    for i in range(24):
        ang = math.pi * i / 12
        r = radius if i % 2 == 0 else radius * 0.45
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    pen.polygon(pts, fill=fill)


# ---------------------------------------------------------------- pictures

def paint_kryvyi(pen, left, top, right, bottom):
    """Kryvyi Rih at night: missile trails falling on a dark skyline."""
    pen.rectangle([left, top, right, bottom], fill=(14, 18, 38))
    rng = random.Random(21)
    for _ in range(60):
        sx = rng.randint(left + 6, right - 6)
        sy = rng.randint(top + 6, bottom - 40)
        r = rng.choice([1, 1, 2])
        pen.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(200, 205, 225))
    ground = bottom - 6
    for tx, th, tw in [(left + 14, 34, 30), (left + 56, 52, 26),
                       (left + 96, 30, 28), (left + 138, 62, 26),
                       (left + 178, 40, 28), (left + 220, 56, 26),
                       (left + 262, 34, 28), (left + 304, 48, 26),
                       (left + 346, 30, 28), (left + 388, 58, 26),
                       (left + 430, 36, 28), (left + 472, 50, 26),
                       (left + 514, 32, 28), (left + 556, 54, 26),
                       (left + 598, 36, 28), (left + 640, 48, 26),
                       (left + 682, 32, 28), (left + 724, 56, 26),
                       (left + 766, 38, 28), (left + 808, 52, 26),
                       (left + 850, 34, 28), (left + 892, 46, 26)]:
        pen.rectangle([tx, ground - th, tx + tw, ground], fill=(40, 44, 66))
        wy = ground - th + 7
        while wy < ground - 5:
            wx = tx + 4
            while wx < tx + tw - 3:
                if (wx + wy) % 3 == 0:
                    pen.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 120))
                wx += 8
            wy += 11
    for hx, hy, deg in [(left + 120, top + 26, 62), (left + 330, top + 14, 58),
                        (left + 560, top + 28, 64), (left + 790, top + 16, 56)]:
        a = math.radians(deg)
        pen.line([(hx - 60 * math.cos(a), hy - 60 * math.sin(a)), (hx, hy)],
                 fill=(255, 150, 60), width=3)
        pen.ellipse([hx - 6, hy - 6, hx + 6, hy + 6], fill=(255, 220, 120))
    starburst(pen, left + 210, ground - 62, 13, (245, 158, 11))
    starburst(pen, left + 660, ground - 56, 11, (245, 158, 11))
    pen.rectangle([left, ground, right, bottom], fill=(20, 14, 34))


def paint_cop31(pen, left, top, right, bottom):
    """COP31 overtime: a globe under a hot sun, clock hands past midnight."""
    pen.rectangle([left, top, right, bottom], fill=(214, 232, 240))
    cx = (left + right) // 2 - 40
    cy = top + 44
    pen.ellipse([left + 8, top + 6, left + 34, top + 32], fill=(252, 196, 96))
    pen.ellipse([left + 13, top + 11, left + 29, top + 27], fill=(255, 220, 140))
    pen.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=(64, 110, 168))
    for ex, ey, ew, eh, col in [(-20, -18, 22, 20, (96, 160, 110)),
                                (4, 4, 18, 16, (96, 160, 110)),
                                (-6, -24, 18, 14, (80, 140, 96))]:
        pen.ellipse([cx + ex, cy + ey, cx + ex + ew, cy + ey + eh], fill=col)
    pen.arc([cx - 30, cy - 30, cx + 30, cy + 30], start=270, end=90,
            fill=(180, 205, 225), width=2)
    pen.ellipse([cx - 11, cy - 30, cx + 11, cy + 30],
                outline=(180, 205, 225), width=2)
    kx, ky = right - 42, top + 40
    pen.ellipse([kx - 16, ky - 16, kx + 16, ky + 16], fill=(255, 255, 255),
                outline=(178, 28, 28), width=2)
    pen.line([kx, ky, kx, ky - 11], fill=(178, 28, 28), width=2)
    pen.line([kx, ky, kx + 8, ky + 3], fill=(178, 28, 28), width=2)


def paint_icj(pen, left, top, right, bottom):
    """Peace Palace: courthouse pediment, columns, scales of justice."""
    pen.rectangle([left, top, right, bottom], fill=(238, 230, 208))
    cx = (left + right) // 2
    pen.polygon([(cx - 92, top + 22), (cx + 92, top + 22), (cx, top + 2)],
                fill=(150, 120, 80))
    pen.rectangle([cx - 92, top + 22, cx + 92, top + 28], fill=(120, 94, 60))
    for colx in (cx - 84, cx - 34, cx + 18, cx + 68):
        pen.rectangle([colx, top + 28, colx + 16, bottom - 10],
                      fill=(250, 246, 236), outline=(150, 120, 80), width=1)
    pen.rectangle([left + 10, bottom - 12, right - 10, bottom - 6],
                  fill=(120, 94, 60))
    sx = cx
    sy = top + 34
    pen.line([sx, sy, sx, sy + 20], fill=(90, 70, 50), width=2)
    pen.line([sx - 15, sy + 2, sx + 15, sy + 2], fill=(90, 70, 50), width=2)
    pen.polygon([(sx - 21, sy + 8), (sx - 9, sy + 8), (sx - 15, sy + 15)],
                fill=(178, 28, 28))
    pen.polygon([(sx + 9, sy + 8), (sx + 21, sy + 8), (sx + 15, sy + 15)],
                fill=(178, 28, 28))


def paint_akvan(pen, left, top, right, bottom):
    """Cyclone Akvan: spiral over the Bay of Bengal, rain slanting in."""
    pen.rectangle([left, top, right, bottom], fill=(188, 216, 228))
    cx = (left + right) // 2
    cy = top + 42
    for r, col in [(34, (255, 255, 255)), (26, (120, 150, 180)),
                   (18, (255, 255, 255)), (10, (64, 110, 168))]:
        pen.arc([cx - r, cy - r, cx + r, cy + r], start=200, end=110,
                fill=col, width=4)
    pen.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(178, 28, 28))
    rng = random.Random(7)
    for _ in range(14):
        rx = rng.randint(left + 8, right - 8)
        ry = rng.randint(top + 58, bottom - 8)
        pen.line([rx, ry, rx - 5, ry + 9], fill=(90, 130, 160), width=2)
    pen.rectangle([left, bottom - 8, right, bottom], fill=(64, 110, 140))


def paint_breach(pen, left, top, right, bottom):
    """Vendor breach: a shield with a broken lock on a dark terminal."""
    pen.rectangle([left, top, right, bottom], fill=(24, 28, 44))
    rng = random.Random(3)
    for _ in range(24):
        sx = rng.randint(left + 8, right - 8)
        sy = rng.randint(top + 8, bottom - 8)
        pen.text((sx, sy), rng.choice(["0", "1"]), font=load("plain", 10),
                 fill=(60, 70, 95))
    cx = (left + right) // 2
    cy = top + 42
    pen.polygon([(cx - 30, cy - 22), (cx + 30, cy - 22), (cx + 30, cy + 6),
                 (cx, cy + 30), (cx - 30, cy + 6)], fill=(178, 28, 28))
    pen.polygon([(cx - 22, cy - 16), (cx + 22, cy - 16), (cx + 22, cy + 4),
                 (cx, cy + 22), (cx - 22, cy + 4)], fill=(255, 255, 255))
    pen.ellipse([cx - 7, cy - 8, cx + 7, cy + 6], fill=(24, 28, 44))
    pen.rectangle([cx - 2, cy + 2, cx + 2, cy + 12], fill=(24, 28, 44))


# ---------------------------------------------------------------- layout

CARDS = [
    ("CLIMATE  •  COP31",
     "COP31 spills into overtime in Antalya",
     "Closing plenary suspended Friday night; the draft drops fossil "
     "fuels and a $120bn finance target.",
     paint_cop31),
    ("JUSTICE  •  THE HAGUE",
     "World court: Myanmar committed genocide",
     "The ICJ's first-ever state genocide finding, 9-6: about 10,000 "
     "Rohingya killed in 2017; reparations ordered.",
     paint_icj),
    ("WEATHER  •  INDIA",
     "Cyclone Akvan weakens over Odisha",
     "Landfall near Gopalpur on Friday at 70-80 kmph; 300,000 people "
     "evacuated as heavy rain and flooding continue.",
     paint_akvan),
    ("TECH  •  CYBERSECURITY",
     "JPMorgan, Visa, Mastercard hit in vendor breach",
     "Ransomware group n0n claims customer data from third-party "
     "providers; no payment data taken, banks say.",
     paint_breach),
]

GEOMETRY = [
    (MARGIN, 460, 504, 692),
    (520, 460, SIZE - MARGIN, 692),
    (MARGIN, 704, 504, 936),
    (520, 704, SIZE - MARGIN, 936),
]


def story_card(pen, box, kicker, headline, summary, painter):
    left, top, right, bottom = box
    pen.rectangle(box, fill=PAL["white"], outline=PAL["edge"], width=2)
    painter(pen, left + 2, top + 2, right - 2, top + 86)
    tx = left + 16
    tw = right - 16 - tx
    y = top + 96
    pen.text((tx, y), kicker, font=load("bold", 15), fill=PAL["red"])
    y += 24
    head_face = load("bold", 21)
    for line in flow(pen, headline, head_face, tw)[:2]:
        pen.text((tx, y), line, font=head_face, fill=PAL["ink"])
        y += 26
    y += 4
    body_face = load("plain", 15)
    for line in flow(pen, summary, body_face, tw)[:2]:
        pen.text((tx, y), line, font=body_face, fill=PAL["body"])
        y += 20


def build():
    img = Image.new("RGB", (SIZE, SIZE), PAL["paper"])
    pen = ImageDraw.Draw(img)

    pen.rectangle([0, 0, SIZE, 80], fill=PAL["wine"])
    centred(pen, 13, "THE WORLD IN ONE IMAGE", load("bold", 24), PAL["white"])
    centred(pen, 48, "THE DAY'S NEWS  •  ONE IMAGE", load("plain", 15),
            PAL["sand"])
    pen.rectangle([0, 80, SIZE, 84], fill=PAL["gold"])

    centred(pen, 94, "Saturday, 21 November 2026", load("serif", 44), PAL["ink"])
    pen.line([MARGIN, 152, SIZE - MARGIN, 152], fill=PAL["red"], width=4)
    pen.line([MARGIN, 160, SIZE - MARGIN, 160], fill=PAL["ink"], width=2)

    hero = (MARGIN, 168, SIZE - MARGIN, 448)
    pen.rectangle(hero, fill=PAL["white"], outline=PAL["edge"], width=2)
    paint_kryvyi(pen, hero[0] + 2, hero[1] + 2, hero[2] - 2, hero[1] + 118)
    tx = MARGIN + 20
    tw = SIZE - MARGIN - 20 - tx
    y = hero[1] + 128
    pen.text((tx, y), "UKRAINE WAR", font=load("bold", 16),
             fill=PAL["red"])
    y += 27
    head_face = load("bold", 28)
    for line in flow(pen, "Russian 'double-tap' strike kills boy, 7, and paramedic in Kryvyi Rih",
                     head_face, tw):
        pen.text((tx, y), line, font=head_face, fill=PAL["ink"])
        y += 34
    y += 2
    body_face = load("plain", 18)
    hero_text = ("Two ballistic missiles hit the city centre on World "
                 "Children's Day; a follow-up drone strike targeted "
                 "rescuers. Two killed, 42 injured, 23 apartment blocks "
                 "and a hospital damaged.")
    for line in flow(pen, hero_text, body_face, tw):
        pen.text((tx, y), line, font=body_face, fill=PAL["body"])
        y += 23

    for box, (kicker, headline, summary, painter) in zip(GEOMETRY, CARDS):
        story_card(pen, box, kicker, headline, summary, painter)

    top, bottom = 948, 1002
    pen.rectangle([MARGIN, top, SIZE - MARGIN, bottom], fill=PAL["strip"],
                  outline=PAL["edge"], width=2)
    label = "ALSO TODAY:  "
    lx = MARGIN + 14
    pen.text((lx, top + 10), label, font=load("bold", 17), fill=PAL["red"])
    lw = pen.textlength(label, font=load("bold", 17))
    strip_text = ("Russia attacks Ukraine with 3 ballistic missiles and "
                  "148 drones overnight  •  Ethiopia named host of COP32 "
                  "in 2027  •  39 trains cancelled as Akvan lashes India's "
                  "east coast")
    yy = top + 10
    for line in flow(pen, strip_text, load("plain", 17),
                     SIZE - MARGIN - 14 - (lx + lw))[:2]:
        pen.text((lx + lw, yy), line, font=load("plain", 17), fill=PAL["ink"])
        yy += 22

    img.save("/home/hatch/workspace/makefun/news-image-20261121/entry.png",
             "PNG", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    build()
