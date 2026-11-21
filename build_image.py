#!/usr/bin/env python3
"""Front page for Saturday 21 November 2026.

Renders a 1024x1024 newspaper-style summary of the day's world news
for the make.fun news-image bounty. Everything is drawn with Pillow
primitives (rectangles, ellipses, lines, polygons) so the output is
fully deterministic: running this script twice produces identical bytes.

Layout, top to bottom:
  masthead banner -> dateline -> night-skyline hero art -> hero story
  -> 2x2 grid of smaller stories -> "also today" footer strip.
"""

import math
import random

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- palette

INK = (26, 26, 26)          # near-black body text
PAPER = (247, 241, 222)      # warm cream page background
CARD = (255, 253, 245)       # story card background
MAROON = (124, 15, 30)      # masthead banner
GOLD = (232, 200, 106)       # masthead subtitle + rule
RULE_RED = (166, 25, 46)     # dateline rule + kickers
KICKER = (176, 30, 40)       # section labels
NIGHT = (25, 25, 48)         # hero skyline sky
STEEL = (42, 42, 68)         # skyline buildings
LIT = (245, 215, 110)        # lit windows
FLARE = (240, 138, 36)       # missile trails / explosions
SKY = (214, 232, 240)        # pale blue art backgrounds
SAND = (238, 230, 204)       # footer strip
EDGE = (201, 191, 165)       # card borders
MUTE = (51, 51, 51)          # body copy

W = H = 1024
MARGIN = 28
INNER = W - 2 * MARGIN       # 968

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

_cache = {}


def typeface(size, bold=False, serif=False):
    """Cached font loader."""
    key = (size, bold, serif)
    if key not in _cache:
        path = SERIF_BOLD if serif else (SANS_BOLD if bold else SANS)
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


# ---------------------------------------------------------------- text flow

def split_lines(draw, text, font, max_w):
    """Greedy word wrap; returns a list of lines fitting max_w pixels."""
    lines, current = [], ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= max_w:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def put_lines(draw, x, y, lines, font, fill, leading):
    """Draw stacked lines; returns the y just below the last line."""
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def put_centered(draw, cx, y, text, font, fill):
    draw.text((cx - draw.textlength(text, font=font) / 2, y),
              text, font=font, fill=fill)


# ---------------------------------------------------------------- hero art

def paint_night_city(draw, box, rng):
    """Night skyline: dark sky, lit towers, missile trails, two blasts."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=NIGHT)
    # stars
    for _ in range(46):
        sx = rng.randint(x0 + 4, x1 - 4)
        sy = rng.randint(y0 + 4, y1 - 60)
        r = rng.choice([1, 1, 2])
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(235, 235, 245))
    # towers along the bottom
    cursor = x0
    while cursor < x1 - 20:
        tw = rng.randint(26, 58)
        th = rng.randint(28, 88)
        shade = rng.randint(-6, 10)
        colour = tuple(max(0, min(255, c + shade)) for c in STEEL)
        draw.rectangle([cursor, y1 - th, cursor + tw, y1], fill=colour)
        for _ in range(th // 9):
            wx = rng.randint(cursor + 4, cursor + tw - 7)
            wy = rng.randint(y1 - th + 5, y1 - 8)
            if rng.random() < 0.55:
                draw.rectangle([wx, wy, wx + 3, wy + 4], fill=LIT)
        cursor += tw + rng.randint(2, 9)
    # missile trails falling from the top edge
    for tx in (140, 330, 590, 800):
        tip_y = rng.randint(y1 - 78, y1 - 52)
        draw.line([(tx - 26, y0 + 2), (tx, tip_y)], fill=FLARE, width=3)
        draw.ellipse([tx - 7, tip_y - 7, tx + 7, tip_y + 7], fill=(250, 214, 90))
    # two starburst explosions among the towers
    for bx, by in ((235, y1 - 62), (655, y1 - 58)):
        for k in range(9):
            ang = k * 40 + rng.randint(-6, 6)
            dx = math.cos(math.radians(ang)) * 15
            dy = math.sin(math.radians(ang)) * 15
            draw.line([(bx, by), (bx + dx, by + dy)],
                      fill=FLARE if k % 2 else (250, 200, 60), width=2)
        draw.ellipse([bx - 5, by - 5, bx + 5, by + 5], fill=(255, 226, 120))


# ---------------------------------------------------------------- card art

def paint_planet(draw, box):
    """Globe with orbit ring, a small sun and a wall clock."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=SKY)
    cx, cy = (x0 + x1) // 2 - 40, (y0 + y1) // 2 + 6
    draw.ellipse([x0 + 18, y0 + 6, x0 + 58, y0 + 46], fill=(250, 214, 90),
                 outline=(224, 170, 40), width=2)
    draw.ellipse([cx - 46, cy - 46, cx + 46, cy + 46], fill=(52, 110, 190))
    draw.ellipse([cx - 30, cy - 26, cx - 2, cy + 2], fill=(74, 160, 90))
    draw.ellipse([cx + 6, cy + 8, cx + 30, cy + 30], fill=(74, 160, 90))
    draw.ellipse([cx - 58, cy - 58, cx + 58, cy + 58], outline=(255, 255, 255),
                 width=3)
    draw.ellipse([x1 - 62, y0 + 22, x1 - 22, y0 + 62], fill=(255, 255, 255),
                 outline=(176, 30, 40), width=2)
    draw.line([(x1 - 42, y0 + 42), (x1 - 42, y0 + 30)], fill=(176, 30, 40),
              width=2)
    draw.line([(x1 - 42, y0 + 42), (x1 - 30, y0 + 46)], fill=(176, 30, 40),
              width=2)


def paint_court(draw, box):
    """Classical courthouse facade with a small scales emblem."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(240, 234, 214))
    mid = (x0 + x1) // 2
    draw.polygon([(mid - 130, y0 + 34), (mid + 130, y0 + 34),
                  (mid, y0 + 2)], fill=(122, 90, 52))
    for cx in (mid - 96, mid - 48, mid, mid + 48, mid + 96):
        draw.rectangle([cx - 11, y0 + 36, cx + 11, y0 + 86],
                       fill=(252, 250, 240), outline=(190, 180, 150))
    draw.rectangle([x0 + 16, y0 + 86, x1 - 16, y0 + 94], fill=(94, 70, 40))
    # scales of justice, small and red, centred on the facade
    sy = y0 + 56
    draw.line([(mid, sy - 14), (mid, sy + 12)], fill=(176, 30, 40), width=3)
    draw.line([(mid - 26, sy - 14), (mid + 26, sy - 14)],
              fill=(176, 30, 40), width=3)
    for sx in (mid - 26, mid + 26):
        draw.line([(sx, sy - 14), (sx, sy + 2)], fill=(176, 30, 40), width=2)
        draw.polygon([(sx - 9, sy + 2), (sx + 9, sy + 2), (sx, sy + 12)],
                     fill=(176, 30, 40))


def paint_storm(draw, box):
    """Cyclone spiral over a rainy sea, dark band at the bottom."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=SKY)
    cx, cy = (x0 + x1) // 2 + 40, (y0 + y1) // 2 - 4
    for r, col in ((52, (255, 255, 255)), (40, (150, 190, 215)),
                   (28, (255, 255, 255)), (16, (90, 140, 180))):
        draw.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=300,
                 fill=col, width=5)
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(176, 30, 40))
    for rx in range(x0 + 30, x1 - 20, 46):
        draw.line([(rx, y1 - 34), (rx - 8, y1 - 14)], fill=(70, 110, 150),
                  width=2)
    draw.rectangle([x0, y1 - 12, x1, y1], fill=(52, 96, 140))


def paint_breach(draw, box):
    """Dark panel with scattered binary digits and a shield keyhole."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(16, 18, 38))
    rng = random.Random(7)
    for _ in range(26):
        bx = rng.randint(x0 + 8, x1 - 14)
        by = rng.randint(y0 + 8, y1 - 16)
        draw.text((bx, by), rng.choice("01"),
                  font=typeface(13), fill=(70, 90, 130))
    mid = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    draw.polygon([(mid - 52, cy - 34), (mid + 52, cy - 34),
                  (mid + 52, cy + 6), (mid, cy + 44), (mid - 52, cy + 6)],
                 fill=(176, 30, 40))
    draw.polygon([(mid - 40, cy - 24), (mid + 40, cy - 24),
                  (mid + 40, cy + 2), (mid, cy + 32), (mid - 40, cy + 2)],
                 fill=(245, 245, 245))
    draw.ellipse([mid - 9, cy - 12, mid + 9, cy + 6], fill=INK)
    draw.polygon([(mid - 5, cy + 2), (mid + 5, cy + 2), (mid + 9, cy + 18),
                  (mid - 9, cy + 18)], fill=INK)


# ---------------------------------------------------------------- stories

HERO = {
    "kicker": "UKRAINE WAR",
    "headline": "Russian \u2018double-tap\u2019 strike kills boy, 7, and "
                "paramedic in Kryvyi Rih",
    "body": "Two ballistic missiles hit the city centre on World "
            "Children\u2019s Day; a follow-up drone strike targeted "
            "rescuers. Two killed, 42 injured, 23 apartment blocks and "
            "a hospital damaged.",
}

GRID = [
    {
        "kicker": "CLIMATE \u2022 COP31",
        "headline": "COP31 spills into overtime in Antalya",
        "body": "Closing plenary suspended Friday night; the draft drops "
                "fossil fuels and a $120bn finance target.",
        "art": paint_planet,
    },
    {
        "kicker": "JUSTICE \u2022 THE HAGUE",
        "headline": "World court: Myanmar committed genocide",
        "body": "The ICJ\u2019s first-ever state genocide finding, 9\u20136: "
                "about 10,000 Rohingya killed in 2017; reparations ordered.",
        "art": paint_court,
    },
    {
        "kicker": "WEATHER \u2022 INDIA",
        "headline": "Cyclone Akvan weakens over Odisha",
        "body": "Landfall near Gopalpur on Friday at 70\u201380 kmph; "
                "300,000 people evacuated as heavy rain and flooding "
                "continue.",
        "art": paint_storm,
    },
    {
        "kicker": "TECH \u2022 CYBERSECURITY",
        "headline": "JPMorgan, Visa, Mastercard hit in vendor breach",
        "body": "Ransomware group n0n claims customer data from "
                "third-party providers; no payment data taken, banks say.",
        "art": paint_breach,
    },
]

FOOTER_LABEL = "ALSO TODAY:"
FOOTER_TEXT = ("Russia attacks Ukraine with 3 ballistic missiles and 148 "
               "drones overnight \u2022 Ethiopia named host of COP32 in "
               "2027 \u2022 39 trains cancelled as Akvan lashes India\u2019s "
               "east coast")


# ---------------------------------------------------------------- assembly

def draw_card(draw, box, story):
    """One grid card: art band on top, kicker, headline, body below."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=CARD, outline=EDGE, width=1)
    story["art"](draw, (x0, y0, x1, y0 + 80))
    tx = x0 + 14
    draw.text((tx, y0 + 90), story["kicker"],
              font=typeface(19, bold=True), fill=KICKER)
    head = split_lines(draw, story["headline"], typeface(25, bold=True),
                       (x1 - x0) - 28)
    y = put_lines(draw, tx, y0 + 112, head, typeface(25, bold=True), INK, 27)
    body = split_lines(draw, story["body"], typeface(18), (x1 - x0) - 28)
    put_lines(draw, tx, y + 4, body, typeface(18), MUTE, 20)


def draw_footer(draw, box):
    """Beige strip: red label inline with two lines of briefs."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=SAND, outline=EDGE, width=1)
    label_font = typeface(19, bold=True)
    text_font = typeface(19)
    label_w = draw.textlength(FOOTER_LABEL + " ", font=label_font)
    first_w = (x1 - x0) - 28 - label_w
    rest_w = (x1 - x0) - 28
    words = FOOTER_TEXT.split()
    lines, cur = [], ""
    limit = first_w
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=text_font) <= limit:
            cur = trial
        else:
            lines.append(cur)
            cur, limit = word, rest_w
    if cur:
        lines.append(cur)
    draw.text((x0 + 14, y0 + 6), FOOTER_LABEL, font=label_font, fill=KICKER)
    y = y0 + 6
    for i, line in enumerate(lines):
        lx = x0 + 14 + (label_w if i == 0 else 0)
        draw.text((lx, y), line, font=text_font, fill=INK)
        y += 21


def build():
    rng = random.Random(20261121)
    page = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(page)

    # masthead banner
    draw.rectangle([0, 0, W, 84], fill=MAROON)
    put_centered(draw, W // 2, 12, "THE WORLD IN ONE IMAGE",
                 typeface(38, bold=True), (255, 255, 255))
    put_centered(draw, W // 2, 54, "THE DAY\u2019S NEWS \u2022 ONE IMAGE",
                 typeface(19), GOLD)
    draw.rectangle([0, 84, W, 88], fill=(217, 164, 65))

    # dateline
    put_centered(draw, W // 2, 102, "Saturday, 21 November 2026",
                 typeface(52, serif=True), INK)
    draw.rectangle([MARGIN, 158, W - MARGIN, 161], fill=RULE_RED)
    draw.rectangle([MARGIN, 164, W - MARGIN, 165], fill=INK)

    # hero skyline + hero story
    paint_night_city(draw, (MARGIN, 172, W - MARGIN, 288), rng)
    draw.rectangle([MARGIN, 288, W - MARGIN, 462], fill=CARD,
                   outline=EDGE, width=1)
    draw.text((MARGIN + 16, 300), HERO["kicker"],
              font=typeface(21, bold=True), fill=KICKER)
    head = split_lines(draw, HERO["headline"], typeface(37, bold=True),
                       INNER - 32)
    y = put_lines(draw, MARGIN + 16, 324, head, typeface(37, bold=True),
                  INK, 42)
    body = split_lines(draw, HERO["body"], typeface(20), INNER - 32)
    put_lines(draw, MARGIN + 16, y + 6, body, typeface(20), MUTE, 25)

    # 2x2 grid of smaller stories
    card_w = (INNER - 16) // 2
    card_h = 236
    top = 468
    for i, story in enumerate(GRID):
        cx = MARGIN + (i % 2) * (card_w + 16)
        cy = top + (i // 2) * (card_h + 10)
        draw_card(draw, (cx, cy, cx + card_w, cy + card_h), story)

    # footer strip
    draw_footer(draw, (MARGIN, 958, W - MARGIN, 1008))

    page.save("entry.png", format="PNG")
    print("wrote entry.png (1024x1024)")


if __name__ == "__main__":
    build()
