#!/usr/bin/env python3
"""The World Today, v4 - Saturday 21 November 2026.
One 1024x1024 front page, 43 dated stories, 13 illustrated cards.
Drawn with Pillow. No network, no randomness, no clock: the same
input always produces the same PNG bytes."""
import os
from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
PAPER = (247, 241, 222)
BLACK = (17, 17, 17)
CRIMSON = (178, 34, 34)
DARKBLUE = (16, 42, 90)
TEAL = (0, 110, 110)
CREAM = (255, 252, 240)
GREY = (60, 60, 60)
FONTS = "/usr/share/fonts/truetype/dejavu"

def load(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)

TITLE_F = load("DejaVuSerif-Bold.ttf", 62)
SUB_F = load("DejaVuSerif.ttf", 17)
SMALL_F = load("DejaVuSans.ttf", 11)
SMALLB_F = load("DejaVuSans-Bold.ttf", 11)
BIG_F = load("DejaVuSerif-Bold.ttf", 26)
SMALLNUM_F = load("DejaVuSans.ttf", 10)
HEAD_F = load("DejaVuSerif-Bold.ttf", 15)
HEADS_F = load("DejaVuSerif-Bold.ttf", 12)
BODY_F = load("DejaVuSans.ttf", 11)
BODYS_F = load("DejaVuSans.ttf", 10)
TAG_F = load("DejaVuSans-Bold.ttf", 10)
LIST_F = load("DejaVuSans.ttf", 10)

def split_lines(d, text, fnt, max_w):
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out

def centred(d, y, text, fnt, fill=BLACK):
    w = d.textlength(text, font=fnt)
    d.text(((PAGE_W - w) / 2, y), text, font=fnt, fill=fill)

# Each card: number, place tag, picture kind, headline, summary.
HERO_CARDS = [
    dict(n=1, place="ANTALYA, TURKIYE - CLIMATE", pic="globe",
         head="COP31 runs into overtime with no deal",
         body="Talks pass the Friday deadline; a third draft is due Saturday morning, still with no mention of fossil fuels. (AP, Al Jazeera)"),
    dict(n=2, place="RIYADH - CONFLICT", pic="missile",
         head="Coalition downs three missiles over Riyadh",
         body="Air defences destroy three ballistic missiles fired at the capital early Saturday, a third straight night of alerts. (Reuters)"),
    dict(n=3, place="JUNIN, PERU - QUAKE", pic="quake",
         head="Magnitude 6.7 earthquake shakes central Peru",
         body="The deep quake struck at 00:09 GMT near Junin, felt in Lima. No deaths, damage or tsunami risk reported. (USGS)"),
]
SMALL_CARDS = [
    dict(n=4, place="DAVAO - AVIATION", pic="plane",
         head="Jet lands safely after engine-fire alert",
         body="Air Niugini 767 diverts after midnight; all 146 aboard safe. (AP)"),
    dict(n=5, place="MERCURY - SPACE", pic="mercury",
         head="BepiColombo reaches Mercury",
         body="Thrusters fire at 19:24 CET tonight after an 8-year voyage. (ESA)"),
    dict(n=6, place="WARSAW - NATO", pic="nato",
         head="Rutte flies to Warsaw for NATO talks",
         body="NATO chief visits a day after the airspace incursion. (AP)"),
    dict(n=7, place="LAS VEGAS - F1", pic="f1",
         head="Las Vegas GP qualifying today",
         body="Grid decided tonight under the lights; Russell fastest in final practice. (F1)"),
    dict(n=8, place="WELLINGTON - CRICKET", pic="cricket",
         head="Rahul hits 136 as India fight back",
         body="India 466/4 lead NZ by 118 at stumps on day 3. (ESPNcricinfo)"),
    dict(n=9, place="BAYELSA - DISASTER", pic="boat",
         head="Nigeria funeral boat capsizes",
         body="At least four dead, two of them children, in Bayelsa. (Reuters)"),
    dict(n=10, place="WORLD - MARKETS", pic="bitcoin",
         head="Bitcoin trades below $59,000",
         body="Down 3.9% in 24 hours; ether $1,625. S&P in correction. (CoinGecko)"),
    dict(n=11, place="HORMUZ - CLAIM", pic="drone",
         head="Iran says it shot down a US MQ-9",
         body="The 58th claim, no US confirmation. (Al Jazeera)"),
    dict(n=12, place="TURIN - TENNIS", pic="tennis",
         head="Medvedev meets Zverev tonight",
         body="Top four meet in the semi-finals tonight. (ATP)"),
    dict(n=13, place="CANBERRA - AI", pic="ai",
         head="Australia and China agree to AI talks",
         body="Albanese ends an 11-day trip with a deal on AI. (ABC)"),
]
MORE = [
    "14 Kyiv: Zelensky warns Crimea bridge 'will not stay' (NBC)",
    "15 Copenhagen: Russian attack expelled over a plot (Al Jazeera)",
    "16 Antalya: EU warns COP31 risks a 'fossil summit' (AFP)",
    "17 Antalya: Panama threatens to block the climate text (Al Jazeera)",
    "18 Jakarta: PLN signs clean-power deals (Antara)",
    "19 Yemen: Houthis threaten Jeddah and Red Sea ports (Al Jazeera)",
    "20 Washington: Vance speaks on the Iran strikes (Reuters)",
    "21 Washington: Lawmaker threatens SpaceX funding (CNN)",
    "22 Texas: Execution of a man of 70 takes 63 minutes (ABC)",
    "23 Los Angeles: Jury convicts man of starting Palisades fire (ABC)",
    "24 Missouri: Judge approves $7.25bn Roundup settlement (AFP)",
    "25 Vancouver: Canada rests defence in youth climate trial (AFP)",
    "26 Pyongyang: Kim tours factories after no Trump meeting (AFP)",
    "27 Sejong: Freight train derails, no one hurt (Korea Herald)",
    "28 Taipei: Budget and cash payout are passed (Taipei Times)",
    "29 Bangkok: Six-point plan on arsenic in two rivers (The Nation)",
    "30 New Delhi: Pakistani minister joins SCO forum in India (Dawn)",
    "31 Myanmar: Rights groups urge sanctions after court ruling (AP)",
    "32 Eastern India: Rain alerts as Akvan's remnant passes (ETV)",
    "33 Port Louis: African ratings agency talks to 15 states (Al Jazeera)",
    "34 Melbourne: Cummins keeps the Australian captaincy (ABC)",
    "35 Las Vegas: Verstappen sent to stewards after contact (Autosport)",
    "36 Seoul: South Korea moves to impeach chief justice (Reuters)",
    "37 Kathmandu: Nepal PM Balendra Shah heads to India (PTI)",
    "38 Nairobi: Kenya begins onshore crude drilling in Turkana (Reuters)",
    "39 Dar es Salaam: Tanzania's Lissu convicted of sedition (AFP)",
    "40 Johannesburg: Nearly 600 women killed in 3 months (Reuters)",
    "41 Baghdad: Basra power-plant fire kills at least 4 (AP)",
    "42 Madrid: Spain heads to 29 Nov election (Reuters)",
    "43 Tallinn: Estonia closes Russia border crossings (AP)",
]

def picture(d, kind, x, y, w, h):
    """One small flat picture per card, drawn in code."""
    d.rectangle([x, y, x + w, y + h], fill=(235, 228, 205))
    cx, cy = x + w // 2, y + h // 2
    if kind == "globe":
        d.ellipse([x + 12, y + 8, x + 62, y + h - 8], fill=(70, 140, 200))
        d.ellipse([x + 26, y + 16, x + 44, y + 34], fill=(90, 180, 90))
        d.ellipse([x + 36, y + 44, x + 56, y + 62], fill=(90, 180, 90))
        d.rectangle([x + w - 34, y + 10, x + w - 26, y + h - 10], fill=CRIMSON)
        d.ellipse([x + w - 36, y + 6, x + w - 24, y + 18], fill=CRIMSON)
    elif kind == "missile":
        d.rectangle([x, y, x + w, y + h], fill=DARKBLUE)
        for bx in (x + 14, x + 52, x + 90):
            d.rectangle([bx, y + h - 34, bx + 26, y + h - 8], fill=(60, 60, 80))
            for wy in range(y + h - 30, y + h - 10, 6):
                d.rectangle([bx + 4, wy, bx + 8, wy + 3], fill=(255, 220, 80))
                d.rectangle([bx + 16, wy, bx + 20, wy + 3], fill=(255, 220, 80))
        for sx, sy in ((x + 30, y + 14), (x + 70, y + 26), (x + 105, y + 10)):
            d.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=(255, 200, 40))
            d.line([sx, sy, sx + 14, sy + 12], fill=(255, 200, 40), width=2)
    elif kind == "quake":
        d.rectangle([x, y, x + w, y + h], fill=(240, 220, 190))
        trace = [(x + 6, cy), (x + 26, cy - 6), (x + 40, cy + 18), (x + 52, cy - 26),
                 (x + 64, cy + 22), (x + 78, cy - 8), (x + 96, cy + 4), (x + w - 6, cy - 10)]
        d.line(trace, fill=CRIMSON, width=3)
        d.polygon([(x + w - 44, y + h - 22), (x + w - 30, y + h - 44), (x + w - 16, y + h - 22)], fill=(120, 90, 60))
        d.polygon([(x + 8, y + h - 22), (x + 20, y + h - 40), (x + 32, y + h - 22)], fill=(140, 140, 140))
    elif kind == "plane":
        d.rectangle([x, y, x + w, y + h], fill=(200, 225, 240))
        d.ellipse([cx - 34, cy - 10, cx + 34, cy + 10], fill=(255, 255, 255), outline=BLACK, width=2)
        d.polygon([(cx + 20, cy - 8), (cx + 44, cy - 16), (cx + 40, cy - 2)], fill=(255, 255, 255), outline=BLACK)
        d.polygon([(cx - 6, cy + 8), (cx + 10, cy + 22), (cx + 16, cy + 8)], fill=(255, 255, 255), outline=BLACK)
        d.ellipse([x + 10, y + 8, x + 26, y + 24], fill=(255, 255, 255))
        d.ellipse([x + 34, y + 16, x + 52, y + 32], fill=(255, 255, 255))
    elif kind == "mercury":
        d.rectangle([x, y, x + w, y + h], fill=(30, 30, 50))
        d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=(180, 170, 150))
        d.ellipse([cx - 12, cy - 8, cx - 2, cy + 2], fill=(140, 130, 110))
        d.ellipse([cx + 6, cy + 6, cx + 14, cy + 14], fill=(140, 130, 110))
        for sx, sy in ((x + 14, y + 12), (x + 100, y + 16), (x + 60, y + 70)):
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    elif kind == "nato":
        d.rectangle([x, y, x + w, y + h], fill=(20, 60, 120))
        for i in range(5):
            sx = x + 16 + i * 20
            d.ellipse([sx - 4, cy - 4, sx + 4, cy + 4], fill=(255, 220, 80))
        d.polygon([(cx, y + 12), (cx + 8, cy + 6), (cx - 8, cy + 6)], fill=(255, 255, 255))
    elif kind == "f1":
        d.rectangle([x, y, x + w, y + h], fill=(40, 40, 40))
        d.line([(x + 8, y + h - 16), (x + 40, y + 20), (x + 80, y + h - 24), (x + w - 8, y + 16)], fill=(255, 255, 255), width=3)
        d.rectangle([cx - 14, cy - 8, cx + 14, cy + 8], fill=CRIMSON)
        d.text((cx - 7, cy - 7), "F1", font=TAG_F, fill=(255, 255, 255))
    elif kind == "cricket":
        d.rectangle([x, y, x + w, y + h], fill=(30, 130, 60))
        d.rectangle([x + 10, y + h - 26, x + w - 10, y + h - 8], fill=(120, 200, 90))
        d.rectangle([cx - 4, y + 12, cx + 4, y + 40], fill=(200, 160, 90))
        d.ellipse([cx - 14, y + 36, cx + 14, y + h - 4], fill=(200, 160, 90))
        d.ellipse([x + w - 26, y + 12, x + w - 14, y + 24], fill=CRIMSON)
    elif kind == "boat":
        d.rectangle([x, y, x + w, y + h], fill=(180, 210, 235))
        d.line([(x + 8, cy + 18), (x + w - 8, cy + 18)], fill=(40, 90, 160), width=3)
        d.polygon([(cx - 30, cy + 18), (cx + 30, cy + 18), (cx + 20, cy + 34), (cx - 20, cy + 34)], fill=(150, 90, 40))
        d.line([(cx, cy - 22), (cx, cy + 18)], fill=BLACK, width=2)
        d.polygon([(cx + 2, cy - 22), (cx + 2, cy + 8), (cx + 20, cy + 8)], fill=(255, 255, 255), outline=BLACK)
    elif kind == "bitcoin":
        d.rectangle([x, y, x + w, y + h], fill=(250, 240, 200))
        chart = [(x + 8, y + 18), (x + 32, y + 34), (x + 52, y + 22), (x + 76, y + 44), (x + w - 8, y + 54)]
        d.line(chart, fill=CRIMSON, width=3)
        d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(255, 180, 40))
        d.text((cx - 6, cy - 9), "B", font=TAG_F, fill=(255, 255, 255))
    elif kind == "drone":
        d.rectangle([x, y, x + w, y + h], fill=(90, 140, 180))
        d.ellipse([cx - 20, cy - 8, cx + 20, cy + 8], fill=(60, 60, 60))
        d.ellipse([cx - 30, cy - 16, cx - 10, cy - 10], fill=(200, 200, 200))
        d.ellipse([cx + 10, cy - 16, cx + 30, cy - 10], fill=(200, 200, 200))
        d.line([(cx, cy + 8), (cx, cy + 26)], fill=(60, 60, 60), width=2)
    elif kind == "tennis":
        d.rectangle([x, y, x + w, y + h], fill=(60, 120, 200))
        d.rectangle([x + 8, y + h - 30, x + w - 8, y + h - 10], fill=(90, 180, 90))
        d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(220, 240, 80), outline=(255, 255, 255), width=2)
        d.arc([cx - 16, cy - 16, cx + 16, cy + 16], 300, 60, fill=(255, 255, 255), width=2)
    elif kind == "ai":
        d.rectangle([x, y, x + w, y + h], fill=(220, 230, 250))
        d.rectangle([x + 16, y + 14, x + w - 16, y + h - 14], fill=(255, 255, 255), outline=DARKBLUE, width=2)
        d.text((x + 24, y + 22), "AI", font=BIG_F, fill=DARKBLUE)
        d.line([(x + 20, y + h - 24), (x + 44, y + h - 34), (x + 64, y + h - 28), (x + w - 20, y + h - 40)], fill=TEAL, width=2)

def draw_card(d, x, y, w, h, card, hero=False):
    d.rectangle([x, y, x + w, y + h], outline=BLACK, width=1, fill=CREAM)
    pic_h = 78 if hero else 52
    picture(d, card["pic"], x + 1, y + 1, w - 2, pic_h)
    ty = y + pic_h + 4
    d.text((x + 6, ty), f"{card['n']}  {card['place']}", font=TAG_F, fill=CRIMSON)
    ty += 13
    hf = HEAD_F if hero else HEADS_F
    for ln in split_lines(d, card["head"], hf, w - 12)[:3 if hero else 2]:
        d.text((x + 6, ty), ln, font=hf, fill=BLACK)
        ty += 18 if hero else 15
    bf = BODY_F if hero else BODYS_F
    step = 14 if hero else 12
    for ln in split_lines(d, card["body"], bf, w - 12)[:3 if hero else 2]:
        d.text((x + 6, ty), ln, font=bf, fill=GREY)
        ty += step

def build():
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    d = ImageDraw.Draw(img)
    d.text((16, 10), "THE WORLD IN ONE DAY", font=SMALLB_F, fill=CRIMSON)
    right = "43 STORIES  •  7 REGIONS  •  EVERY ONE DATED SATURDAY 21 NOVEMBER 2026"
    d.text((PAGE_W - 16 - d.textlength(right, font=SMALLB_F), 10), right, font=SMALLB_F, fill=BLACK)
    d.line([(16, 30), (PAGE_W - 16, 30)], fill=BLACK, width=2)
    centred(d, 36, "Saturday 21 November 2026", TITLE_F)
    centred(d, 104, "COP31 runs into overtime  •  Riyadh downs three missiles  •  A 6.7 quake shakes Peru", SUB_F)
    d.line([(16, 128), (PAGE_W - 16, 128)], fill=BLACK, width=1)
    # Big numbers strip.
    stats = [("13", "days COP31 has run in Antalya, still with no deal"),
             ("3", "ballistic missiles shot down over Riyadh before dawn"),
             ("6.7", "magnitude of the earthquake in Junin, central Peru"),
             ("146", "people safe after a jet's engine-fire alert"),
             ("$58,983", "bitcoin early Saturday, down 3.9% in a day"),
             ("136", "runs by KL Rahul that put India in charge")]
    x = 16
    col_w = (PAGE_W - 32) / 6
    for val, lab in stats:
        d.text((x + 4, 134), val, font=BIG_F, fill=CRIMSON)
        ty = 164
        for ln in split_lines(d, lab, SMALLNUM_F, col_w - 10)[:3]:
            d.text((x + 4, ty), ln, font=SMALLNUM_F, fill=BLACK)
            ty += 11
        x += col_w
        if x < PAGE_W - 16:
            d.line([(x, 136), (x, 196)], fill=CRIMSON, width=1)
    # Region bar, widths proportional to story counts (43 in all).
    parts = [("Europe 11", 11, (20, 60, 140)), ("Asia 10", 10, CRIMSON), ("Middle East 5", 5, (140, 110, 20)),
             ("Africa 4", 4, (30, 120, 60)), ("Americas 8", 8, (110, 50, 140)), ("Oceania 3", 3, TEAL), ("Glob 2", 2, (80, 80, 80))]
    x = 16
    for name, count, col in parts:
        seg = (PAGE_W - 32) * count / 43
        d.rectangle([x, 200, x + seg, 218], fill=col)
        d.text((x + 4, 203), name, font=SMALLB_F, fill=(255, 255, 255))
        x += seg
    # Hero row of three.
    hero_w = (PAGE_W - 32 - 16) / 3
    for i, card in enumerate(HERO_CARDS):
        draw_card(d, 16 + i * (hero_w + 8), 226, hero_w, 172, card, hero=True)
    # Two rows of five small cards.
    small_w = (PAGE_W - 32 - 32) / 5
    y = 406
    for r in range(2):
        for i in range(5):
            draw_card(d, 16 + i * (small_w + 8), y, small_w, 138, SMALL_CARDS[r * 5 + i])
        y += 146
    # Map and the rest of the stories.
    y = 700
    d.text((16, y), "WHERE IT HAPPENED", font=SMALLB_F, fill=CRIMSON)
    d.text((330, y), "ALSO ON SATURDAY 21 NOVEMBER 2026  —  30 MORE STORIES  •  43 IN ALL", font=SMALLB_F, fill=CRIMSON)
    mx, my, mw, mh = 16, y + 18, 300, 150
    d.rectangle([mx, my, mx + mw, my + mh], fill=(200, 225, 240), outline=BLACK)
    for bx, by, bw, bh in [(30, 30, 70, 40), (110, 20, 60, 36), (180, 44, 66, 40), (60, 80, 80, 44), (200, 90, 50, 30), (250, 130, 34, 16)]:
        d.ellipse([mx + bx, my + by, mx + bx + bw, my + by + bh], fill=(230, 215, 160))
    for i, (px, py) in enumerate([(48, 42), (128, 34), (196, 58), (84, 96), (214, 104), (262, 138), (70, 52), (150, 70)]):
        d.ellipse([mx + px - 6, my + py - 6, mx + px + 6, my + py + 6], fill=CRIMSON, outline=(255, 255, 255))
        d.text((mx + px - 3, my + py - 5), str(i + 1), font=SMALLB_F, fill=(255, 255, 255))
    d.text((mx + 10, my + 6), "PACIFIC", font=SMALLB_F, fill=(60, 90, 140))
    d.text((mx + 120, my + 130), "ATLANTIC", font=SMALLB_F, fill=(60, 90, 140))
    d.text((16, y + 172), "Red numbers mark stories 1-13.", font=SMALL_F, fill=(80, 80, 80))
    for i, s in enumerate(MORE):
        col = i // 15
        row = i % 15
        d.text((330 + col * 330, y + 18 + row * 11), s, font=LIST_F, fill=BLACK)
    # Date check box.
    by = 892
    d.rectangle([16, by, PAGE_W - 16, by + 76], outline=CRIMSON, width=2)
    d.text((24, by + 6), "DATE CHECK  ✓", font=SMALLB_F, fill=CRIMSON)
    note = ("Every story here happened, or was first reported, on Saturday 21 November 2026. LEFT OUT — other days' news: "
            "Russian missiles land in Poland (Fri 20 Nov) • Kyiv bridges hit (Fri 20 Nov) • UK–EU deal (Fri 20 Nov) • "
            "ICJ Myanmar genocide ruling (Thu 19 Nov) • Cyclone Akvan's landfall (Fri 20 Nov) • Anthropic debut, shares jump 17% (Thu 19 Nov).")
    ty = by + 22
    for ln in split_lines(d, note, BODYS_F, PAGE_W - 48):
        d.text((24, ty), ln, font=BODYS_F, fill=BLACK)
        ty += 13
    d.text((16, 978), "Every story here happened, or was first reported, on Saturday 21 November 2026. Officials' counts and claims are attributed.",
           font=SMALL_F, fill=(80, 80, 80))
    d.text((16, 996), "Sources: Reuters, AP, AFP, BBC, Al Jazeera, USGS, ESA, CoinGecko  •  Pictures and map: original, drawn in code  •  21 November 2026",
           font=SMALL_F, fill=(80, 80, 80))
    img.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png"))
    print("saved entry.png", img.size)

if __name__ == "__main__":
    build()
