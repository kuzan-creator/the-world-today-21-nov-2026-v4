#!/usr/bin/env python3
"""Draw v4 of The World Today - 21 Nov 2026: 43 dated stories, 13 illustrated cards.
Deterministic, no network, no random, no timestamps. Pillow only.
v4 rebuilds the proven v2 design fresh: same 43 stories, same flat illustrations,
same layout — with three small fixes only: the cricket bat no longer spills out of
its picture, the boat gets its sail, and the map gets ocean labels."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1024, 1024
BG = (247, 241, 222)
INK = (17, 17, 17)
RED = (178, 34, 34)
NAVY = (16, 42, 90)
TEAL = (0, 110, 110)
FONTDIR = "/usr/share/fonts/truetype/dejavu"

def font(name, size):
    return ImageFont.truetype(os.path.join(FONTDIR, name), size)

F_TITLE = font("DejaVuSerif-Bold.ttf", 62)
F_SUB = font("DejaVuSerif.ttf", 17)
F_SMALL = font("DejaVuSans.ttf", 11)
F_SMALLB = font("DejaVuSans-Bold.ttf", 11)
F_NUM = font("DejaVuSerif-Bold.ttf", 26)
F_NUMS = font("DejaVuSans.ttf", 10)
F_HEAD = font("DejaVuSerif-Bold.ttf", 15)
F_HEAD_S = font("DejaVuSerif-Bold.ttf", 12)
F_BODY = font("DejaVuSans.ttf", 11)
F_BODY_S = font("DejaVuSans.ttf", 10)
F_TAG = font("DejaVuSans-Bold.ttf", 10)
F_LIST = font("DejaVuSans.ttf", 10)

def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def center(draw, y, text, fnt, fill=INK, x0=0, x1=W):
    w = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)

# ---------- illustrations: simple flat drawings, one per card ----------
def illu(draw, kind, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(235, 228, 205))
    cx, cy = x + w / 2, y + h / 2
    if kind == "globe":
        draw.ellipse([x + 12, y + 8, x + 62, y + h - 8], fill=(70, 140, 200))
        draw.ellipse([x + 26, y + 16, x + 44, y + 34], fill=(90, 180, 90))
        draw.ellipse([x + 36, y + 44, x + 56, y + 62], fill=(90, 180, 90))
        draw.rectangle([x + w - 34, y + 10, x + w - 26, y + h - 10], fill=RED)
        draw.ellipse([x + w - 36, y + 6, x + w - 24, y + 18], fill=RED)
    elif kind == "missile":
        draw.rectangle([x, y, x + w, y + h], fill=NAVY)
        for bx in [x + 14, x + 52, x + 90]:
            draw.rectangle([bx, y + h - 34, bx + 26, y + h - 8], fill=(60, 60, 80))
            for wy in range(y + h - 30, y + h - 10, 6):
                draw.rectangle([bx + 4, wy, bx + 8, wy + 3], fill=(255, 220, 80))
                draw.rectangle([bx + 16, wy, bx + 20, wy + 3], fill=(255, 220, 80))
        for sx, sy in [(x + 30, y + 14), (x + 70, y + 26), (x + 105, y + 10)]:
            draw.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=(255, 200, 40))
            draw.line([sx, sy, sx + 14, sy + 12], fill=(255, 200, 40), width=2)
    elif kind == "quake":
        draw.rectangle([x, y, x + w, y + h], fill=(240, 220, 190))
        pts = [(x + 6, cy), (x + 26, cy - 6), (x + 40, cy + 18), (x + 52, cy - 26),
               (x + 64, cy + 22), (x + 78, cy - 8), (x + 96, cy + 4), (x + w - 6, cy - 10)]
        draw.line(pts, fill=RED, width=3)
        draw.polygon([(x + w - 44, y + h - 22), (x + w - 30, y + h - 44), (x + w - 16, y + h - 22)], fill=(120, 90, 60))
        draw.polygon([(x + 8, y + h - 22), (x + 20, y + h - 40), (x + 32, y + h - 22)], fill=(140, 140, 140))
    elif kind == "plane":
        draw.rectangle([x, y, x + w, y + h], fill=(200, 225, 240))
        draw.ellipse([cx - 34, cy - 10, cx + 34, cy + 10], fill=(255, 255, 255), outline=INK, width=2)
        draw.polygon([(cx + 20, cy - 8), (cx + 44, cy - 16), (cx + 40, cy - 2)], fill=(255, 255, 255), outline=INK)
        draw.polygon([(cx - 6, cy + 8), (cx + 10, cy + 22), (cx + 16, cy + 8)], fill=(255, 255, 255), outline=INK)
        draw.ellipse([x + 10, y + 8, x + 26, y + 24], fill=(255, 255, 255))
        draw.ellipse([x + 34, y + 16, x + 52, y + 32], fill=(255, 255, 255))
    elif kind == "mercury":
        draw.rectangle([x, y, x + w, y + h], fill=(30, 30, 50))
        draw.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=(180, 170, 150))
        draw.ellipse([cx - 12, cy - 8, cx - 2, cy + 2], fill=(140, 130, 110))
        draw.ellipse([cx + 6, cy + 6, cx + 14, cy + 14], fill=(140, 130, 110))
        for sx, sy in [(x + 14, y + 12), (x + 100, y + 16), (x + 60, y + 70)]:
            draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    elif kind == "nato":
        draw.rectangle([x, y, x + w, y + h], fill=(20, 60, 120))
        for i in range(5):
            sx = x + 16 + i * 20
            draw.ellipse([sx - 4, cy - 4, sx + 4, cy + 4], fill=(255, 220, 80))
        draw.polygon([(cx, y + 12), (cx + 8, cy + 6), (cx - 8, cy + 6)], fill=(255, 255, 255))
    elif kind == "f1":
        draw.rectangle([x, y, x + w, y + h], fill=(40, 40, 40))
        draw.line([(x + 8, y + h - 16), (x + 40, y + 20), (x + 80, y + h - 24), (x + w - 8, y + 16)], fill=(255, 255, 255), width=3)
        draw.rectangle([cx - 14, cy - 8, cx + 14, cy + 8], fill=RED)
        draw.text((cx - 7, cy - 7), "F1", font=F_TAG, fill=(255, 255, 255))
    elif kind == "cricket":
        draw.rectangle([x, y, x + w, y + h], fill=(30, 130, 60))
        draw.rectangle([x + 10, y + h - 26, x + w - 10, y + h - 8], fill=(120, 200, 90))
        draw.rectangle([cx - 4, y + 12, cx + 4, y + 40], fill=(200, 160, 90))
        draw.ellipse([cx - 14, y + 36, cx + 14, y + h - 4], fill=(200, 160, 90))
        draw.ellipse([x + w - 26, y + 12, x + w - 14, y + 24], fill=RED)
    elif kind == "boat":
        draw.rectangle([x, y, x + w, y + h], fill=(180, 210, 235))
        draw.line([(x + 8, cy + 18), (x + w - 8, cy + 18)], fill=(40, 90, 160), width=3)
        draw.polygon([(cx - 30, cy + 18), (cx + 30, cy + 18), (cx + 20, cy + 34), (cx - 20, cy + 34)], fill=(150, 90, 40))
        draw.line([(cx, cy - 22), (cx, cy + 18)], fill=INK, width=2)
        draw.polygon([(cx + 2, cy - 22), (cx + 2, cy + 8), (cx + 20, cy + 8)], fill=(255, 255, 255), outline=INK)
    elif kind == "bitcoin":
        draw.rectangle([x, y, x + w, y + h], fill=(250, 240, 200))
        pts = [(x + 8, y + 18), (x + 32, y + 34), (x + 52, y + 22), (x + 76, y + 44), (x + w - 8, y + 54)]
        draw.line(pts, fill=RED, width=3)
        draw.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(255, 180, 40))
        draw.text((cx - 6, cy - 9), "B", font=F_TAG, fill=(255, 255, 255))
    elif kind == "drone":
        draw.rectangle([x, y, x + w, y + h], fill=(90, 140, 180))
        draw.ellipse([cx - 20, cy - 8, cx + 20, cy + 8], fill=(60, 60, 60))
        draw.ellipse([cx - 30, cy - 16, cx - 10, cy - 10], fill=(200, 200, 200))
        draw.ellipse([cx + 10, cy - 16, cx + 30, cy - 10], fill=(200, 200, 200))
        draw.line([(cx, cy + 8), (cx, cy + 26)], fill=(60, 60, 60), width=2)
    elif kind == "tennis":
        draw.rectangle([x, y, x + w, y + h], fill=(60, 120, 200))
        draw.rectangle([x + 8, y + h - 30, x + w - 8, y + h - 10], fill=(90, 180, 90))
        draw.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(220, 240, 80), outline=(255, 255, 255), width=2)
        draw.arc([cx - 16, cy - 16, cx + 16, cy + 16], 300, 60, fill=(255, 255, 255), width=2)
    elif kind == "ai":
        draw.rectangle([x, y, x + w, y + h], fill=(220, 230, 250))
        draw.rectangle([x + 16, y + 14, x + w - 16, y + h - 14], fill=(255, 255, 255), outline=NAVY, width=2)
        draw.text((x + 24, y + 22), "AI", font=F_NUM, fill=NAVY)
        draw.line([(x + 20, y + h - 24), (x + 44, y + h - 34), (x + 64, y + h - 28), (x + w - 20, y + h - 40)], fill=TEAL, width=2)

HERO = [
    (1, "ANTALYA, TURKIYE - CLIMATE", "globe", "COP31 runs into overtime with no deal",
     "Talks pass the Friday deadline; a third draft is due Saturday morning, still with no mention of fossil fuels. (AP, Al Jazeera)", "AFP"),
    (2, "RIYADH - CONFLICT", "missile", "Coalition downs three missiles over Riyadh",
     "Air defences destroy three ballistic missiles fired at the capital early Saturday, a third straight night of alerts. (Reuters)", "AFP"),
    (3, "JUNIN, PERU - QUAKE", "quake", "Magnitude 6.7 earthquake shakes central Peru",
     "The deep quake struck at 00:09 GMT near Junin, felt in Lima. No deaths, damage or tsunami risk reported. (USGS)", "USGS"),
]
SMALL = [
    (4, "DAVAO - AVIATION", "plane", "Jet lands safely after engine-fire alert",
     "Air Niugini 767 diverts after midnight; all 146 aboard safe. (AP)", "AP"),
    (5, "MERCURY - SPACE", "mercury", "BepiColombo reaches Mercury",
     "Thrusters fire at 19:24 CET tonight after an 8-year voyage. (ESA)", "ESA"),
    (6, "WARSAW - NATO", "nato", "Rutte flies to Warsaw for NATO talks",
     "NATO chief visits a day after the airspace incursion. (AP)", "AP"),
    (7, "LAS VEGAS - F1", "f1", "Las Vegas GP qualifying today",
     "Grid decided tonight under the lights; Russell fastest in final practice. (F1)", "F1"),
    (8, "WELLINGTON - CRICKET", "cricket", "Rahul hits 136 as India fight back",
     "India 466/4 lead NZ by 118 at stumps on day 3. (ESPNcricinfo)", "ESPN"),
    (9, "BAYELSA - DISASTER", "boat", "Nigeria funeral boat capsizes",
     "At least four dead, two of them children, in Bayelsa. (Reuters)", "Reuters"),
    (10, "WORLD - MARKETS", "bitcoin", "Bitcoin trades below $59,000",
     "Down 3.9% in 24 hours; ether $1,625. S&P in correction. (CoinGecko)", "CoinGecko"),
    (11, "HORMUZ - CLAIM", "drone", "Iran says it shot down a US MQ-9",
     "The 58th claim, no US confirmation. (Al Jazeera)", "Al Jazeera"),
    (12, "TURIN - TENNIS", "tennis", "Medvedev meets Zverev tonight",
     "Top four meet in the semi-finals tonight. (ATP)", "ATP"),
    (13, "CANBERRA - AI", "ai", "Australia and China agree to AI talks",
     "Albanese ends an 11-day trip with a deal on AI. (ABC)", "ABC"),
]
ALSO = [
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

def card(draw, x, y, w, h, num, tag, kind, headline, summary, big=False):
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1, fill=(255, 252, 240))
    ih = 78 if big else 52
    illu(draw, kind, x + 1, y + 1, w - 2, ih)
    ty = y + ih + 4
    draw.text((x + 6, ty), f"{num}  {tag}", font=F_TAG, fill=RED)
    ty += 13
    hf = F_HEAD if big else F_HEAD_S
    for ln in wrap(draw, headline, hf, w - 12)[:3 if big else 2]:
        draw.text((x + 6, ty), ln, font=hf, fill=INK)
        ty += 18 if big else 15
    bf = F_BODY if big else F_BODY_S
    lh = 14 if big else 12
    for ln in wrap(draw, summary, bf, w - 12)[:3 if big else 2]:
        draw.text((x + 6, ty), ln, font=bf, fill=(60, 60, 60))
        ty += lh

def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((16, 10), "THE WORLD IN ONE DAY", font=F_SMALLB, fill=RED)
    right = "43 STORIES  •  7 REGIONS  •  EVERY ONE DATED SATURDAY 21 NOVEMBER 2026"
    d.text((W - 16 - d.textlength(right, font=F_SMALLB), 10), right, font=F_SMALLB, fill=INK)
    d.line([(16, 30), (W - 16, 30)], fill=INK, width=2)
    center(d, 36, "Saturday 21 November 2026", F_TITLE)
    center(d, 104, "COP31 runs into overtime  •  Riyadh downs three missiles  •  A 6.7 quake shakes Peru", F_SUB)
    d.line([(16, 128), (W - 16, 128)], fill=INK, width=1)
    nums = [("13", "days COP31 has run in Antalya, still with no deal"),
            ("3", "ballistic missiles shot down over Riyadh before dawn"),
            ("6.7", "magnitude of the earthquake in Junin, central Peru"),
            ("146", "people safe after a jet's engine-fire alert"),
            ("$58,983", "bitcoin early Saturday, down 3.9% in a day"),
            ("136", "runs by KL Rahul that put India in charge")]
    x = 16
    cw = (W - 32) / 6
    for val, lab in nums:
        d.text((x + 4, 134), val, font=F_NUM, fill=RED)
        ty = 164
        for ln in wrap(d, lab, F_NUMS, cw - 10)[:3]:
            d.text((x + 4, ty), ln, font=F_NUMS, fill=INK)
            ty += 11
        x += cw
        if x < W - 16:
            d.line([(x, 136), (x, 196)], fill=RED, width=1)
    regions = [("Europe 11", (20, 60, 140)), ("Asia 10", RED), ("Middle East 5", (140, 110, 20)),
               ("Africa 4", (30, 120, 60)), ("Americas 8", (110, 50, 140)), ("Oceania 3", TEAL), ("Glob 2", (80, 80, 80))]
    x = 16
    total_w = W - 32
    for name, col in regions:
        rw = total_w * {"Europe 11": 11, "Asia 10": 10, "Middle East 5": 5, "Africa 4": 4, "Americas 8": 8, "Oceania 3": 3, "Glob 2": 2}[name] / 43
        d.rectangle([x, 200, x + rw, 218], fill=col)
        d.text((x + 4, 203), name, font=F_SMALLB, fill=(255, 255, 255))
        x += rw
    y = 226
    hw = (W - 32 - 16) / 3
    for i, (num, tag, kind, head, summ, src) in enumerate(HERO):
        card(d, 16 + i * (hw + 8), y, hw, 172, num, tag, kind, head, summ, big=True)
    y = 406
    sw = (W - 32 - 32) / 5
    for r in range(2):
        for i in range(5):
            c = SMALL[r * 5 + i]
            card(d, 16 + i * (sw + 8), y, sw, 138, c[0], c[1], c[2], c[3], c[4], big=False)
        y += 146
    y = 700
    d.text((16, y), "WHERE IT HAPPENED", font=F_SMALLB, fill=RED)
    d.text((330, y), "ALSO ON SATURDAY 21 NOVEMBER 2026  —  30 MORE STORIES  •  43 IN ALL", font=F_SMALLB, fill=RED)
    mx, my, mw, mh = 16, y + 18, 300, 150
    d.rectangle([mx, my, mx + mw, my + mh], fill=(200, 225, 240), outline=INK)
    blobs = [(30, 30, 70, 40), (110, 20, 60, 36), (180, 44, 66, 40), (60, 80, 80, 44), (200, 90, 50, 30), (250, 130, 34, 16)]
    for bx, by, bw, bh in blobs:
        d.ellipse([mx + bx, my + by, mx + bx + bw, my + by + bh], fill=(230, 215, 160))
    pins = [(48, 42), (128, 34), (196, 58), (84, 96), (214, 104), (262, 138), (70, 52), (150, 70)]
    for i, (px, py) in enumerate(pins):
        d.ellipse([mx + px - 6, my + py - 6, mx + px + 6, my + py + 6], fill=RED, outline=(255, 255, 255))
        d.text((mx + px - 3, my + py - 5), str(i + 1), font=F_SMALLB, fill=(255, 255, 255))
    d.text((mx + 10, my + 6), "PACIFIC", font=F_SMALLB, fill=(60, 90, 140))
    d.text((mx + 120, my + 132), "ATLANTIC", font=F_SMALLB, fill=(60, 90, 140))
    d.text((16, y + 172), "Red numbers mark stories 1-13.", font=F_SMALL, fill=(80, 80, 80))
    lx, ly = 330, y + 18
    colw = 330
    for i, s in enumerate(ALSO):
        col = i // 15
        row = i % 15
        d.text((lx + col * colw, ly + row * 11), s, font=F_LIST, fill=INK)
    by = 892
    d.rectangle([16, by, W - 16, by + 76], outline=RED, width=2)
    d.text((24, by + 6), "DATE CHECK  ✓", font=F_SMALLB, fill=RED)
    txt = ("Every story here happened, or was first reported, on Saturday 21 November 2026. LEFT OUT — other days' news: "
           "Russian missiles land in Poland (Fri 20 Nov) • Kyiv bridges hit (Fri 20 Nov) • UK–EU deal (Fri 20 Nov) • "
           "ICJ Myanmar genocide ruling (Thu 19 Nov) • Cyclone Akvan's landfall (Fri 20 Nov) • Anthropic debut, shares jump 17% (Thu 19 Nov).")
    ty = by + 22
    for ln in wrap(d, txt, F_BODY_S, W - 48):
        d.text((24, ty), ln, font=F_BODY_S, fill=INK)
        ty += 13
    d.text((16, 978), "Every story here happened, or was first reported, on Saturday 21 November 2026. Officials' counts and claims are attributed.",
           font=F_SMALL, fill=(80, 80, 80))
    d.text((16, 996), "Sources: Reuters, AP, AFP, BBC, Al Jazeera, USGS, ESA, CoinGecko  •  Pictures and map: original, drawn in code  •  21 November 2026",
           font=F_SMALL, fill=(80, 80, 80))
    img.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png"))
    print("saved entry.png", img.size)

if __name__ == "__main__":
    main()
