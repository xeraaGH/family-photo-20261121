"""Family at home with one machine member — warm kitchen, evening light.

Flat-illustration render in PIL: a family of three relaxed around a kitchen
table while a friendly household robot peels a carrot at the counter.
Specific detail: a dog bowl on the floor, carrot peels on the counter.
No text or lettering anywhere in the frame.
"""
import math
import random

from PIL import Image, ImageDraw, ImageFilter

W = H = 1024
random.seed(7)

# ---- palette (warm evening kitchen) ----
WALL = (238, 214, 178)
WALL_DARK = (226, 196, 152)
FLOOR = (176, 128, 84)
FLOOR_DARK = (158, 112, 70)
FLOOR_LIGHT = (196, 148, 100)
COUNTER = (122, 88, 62)
COUNTER_TOP = (214, 190, 158)
CABINET = (96, 122, 92)
TABLE = (150, 104, 66)
TABLE_TOP = (182, 132, 84)
SKIN_A = (232, 188, 152)
SKIN_B = (214, 164, 124)
SKIN_C = (244, 205, 170)
HAIR_DARK = (62, 44, 34)
HAIR_GREY = (178, 168, 152)
HAIR_BROWN = (110, 72, 44)
SHIRT_BLUE = (84, 112, 148)
SHIRT_RUST = (178, 96, 62)
SHIRT_GREEN = (110, 138, 96)
ROBOT_BODY = (214, 220, 224)
ROBOT_DARK = (150, 158, 164)
ROBOT_ACCENT = (232, 150, 60)
CARROT = (232, 122, 40)
BOWL_BLUE = (70, 104, 140)
GLOW = (255, 214, 140)


def rr(d, box, r, fill):
    d.rounded_rectangle(box, radius=r, fill=fill)


def ell(d, box, fill):
    x0, y0, x1, y1 = box
    d.ellipse([min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)], fill=fill)


def poly(d, pts, fill):
    d.polygon(pts, fill=fill)


def person(d, cx, base_y, h, skin, hair, shirt, hair_style, facing=1):
    """Simple seated figure: head, torso, one arm. base_y = seat level."""
    head_r = int(h * 0.16)
    head_cy = base_y - int(h * 0.82)
    # torso
    rr(d, [cx - int(h * 0.22), head_cy + head_r - 6, cx + int(h * 0.22),
           base_y + int(h * 0.10)], int(h * 0.10), fill=shirt)
    # arm resting toward table
    d.line([(cx + facing * int(h * 0.16), head_cy + int(h * 0.28)),
            (cx + facing * int(h * 0.34), base_y - int(h * 0.05))],
           fill=shirt, width=int(h * 0.07))
    ell(d, [cx + facing * int(h * 0.30), base_y - int(h * 0.10),
            cx + facing * int(h * 0.40), base_y + int(h * 0.02)], fill=skin)
    # head
    ell(d, [cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r], fill=skin)
    # hair
    if hair_style == "bun":
        ell(d, [cx - head_r, head_cy - head_r - 6, cx + head_r, head_cy + 2], fill=hair)
        ell(d, [cx - 12, head_cy - head_r - 22, cx + 12, head_cy - head_r + 2], fill=hair)
    elif hair_style == "short":
        ell(d, [cx - head_r, head_cy - head_r - 4, cx + head_r, head_cy - 2], fill=hair)
    elif hair_style == "long":
        ell(d, [cx - head_r, head_cy - head_r - 4, cx + head_r, head_cy + head_r + 26], fill=hair)
        ell(d, [cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r], fill=skin)
    else:  # child curls
        for dx, dy in [(-16, -14), (0, -20), (16, -14), (-22, -2), (22, -2)]:
            ell(d, [cx + dx - 10, head_cy + dy - 10, cx + dx + 10, head_cy + dy + 10], fill=hair)


img = Image.new("RGB", (W, H), WALL)
d = ImageDraw.Draw(img)

# ---- wall + floor ----
d.rectangle([0, 0, W, 640], fill=WALL)
d.rectangle([0, 640, W, H], fill=FLOOR)
# floor boards
for y in range(660, H, 56):
    d.line([(0, y), (W, y)], fill=FLOOR_DARK, width=3)
for x in range(0, W, 210):
    d.line([(x, 640), (x - 40, H)], fill=FLOOR_DARK, width=2)
# soft wall shadow band above floor
for i in range(40):
    a = int(18 * (1 - i / 40))
    d.line([(0, 600 + i), (W, 600 + i)], fill=(WALL_DARK[0], WALL_DARK[1], WALL_DARK[2]))

# ---- window, top left, evening glow ----
wx0, wy0, wx1, wy1 = 70, 80, 330, 380
rr(d, [wx0 - 12, wy0 - 12, wx1 + 12, wy1 + 12], 10, fill=(250, 244, 228))
for i in range(60):
    t = i / 60
    col = tuple(int(255 - (255 - 244) * t) for _ in range(3))
    col = (255, int(214 - 60 * t), int(140 + 40 * t))
    d.rectangle([wx0, wy0 + int((wy1 - wy0) * t / 1), wx1,
                 wy0 + int((wy1 - wy0) * (t + 1 / 60))], fill=col)
# sun low in window
ell(d, [150, 250, 230, 330], fill=(255, 226, 150))
# window cross bars
d.rectangle([wx0, 215, wx1, 229], fill=(250, 244, 228))
d.rectangle([188, wy0, 202, wy1], fill=(250, 244, 228))
# warm light spill on wall from window
glow = Image.new("RGB", (W, H), (0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([40, 300, 620, 700], fill=(60, 40, 10))
glow = glow.filter(ImageFilter.GaussianBlur(90))
img = Image.composite(Image.blend(img, Image.new("RGB", (W, H), GLOW), 0.18),
                      img, glow.convert("L").point(lambda v: v // 3))
d = ImageDraw.Draw(img)

# ---- wall shelf with jars, top right ----
d.rectangle([700, 150, 980, 168], fill=(140, 98, 62))
for jx, jc in [(730, (196, 120, 80)), (800, (120, 140, 100)), (870, (190, 150, 90)), (930, (150, 110, 90))]:
    rr(d, [jx, 96, jx + 44, 150], 8, fill=jc)
    d.rectangle([jx + 8, 88, jx + 36, 98], fill=(90, 70, 50))

# ---- kitchen counter, right side ----
d.rectangle([640, 520, W, 660], fill=CABINET)
d.rectangle([640, 500, W, 524], fill=COUNTER_TOP)
# cabinet doors
for cx0 in (660, 780, 900):
    d.rectangle([cx0, 540, cx0 + 96, 650], outline=(70, 92, 68), width=3)
    ell(d, [cx0 + 40, 588, cx0 + 56, 604], fill=(210, 200, 180))

# ---- pendant lamp over table ----
d.line([(360, 0), (360, 150)], fill=(70, 60, 50), width=4)
poly(d, [(330, 150), (390, 150), (375, 195), (345, 195)], fill=(60, 52, 44))
ell(d, [340, 195, 380, 215], fill=(255, 220, 140))
# lamp glow
lg = Image.new("RGB", (W, H), (0, 0, 0))
ld = ImageDraw.Draw(lg)
ld.ellipse([180, 180, 540, 560], fill=(70, 50, 14))
lg = lg.filter(ImageFilter.GaussianBlur(70))
img = Image.composite(Image.blend(img, Image.new("RGB", (W, H), (255, 214, 140)), 0.12),
                      img, lg.convert("L").point(lambda v: v // 3))
d = ImageDraw.Draw(img)

# ---- dining table, centre-left ----
# table top (perspective)
poly(d, [(120, 700), (560, 700), (600, 760), (80, 760)], fill=TABLE_TOP)
poly(d, [(80, 760), (600, 760), (600, 782), (80, 782)], fill=TABLE)
# legs
d.rectangle([130, 782, 152, 900], fill=TABLE)
d.rectangle([528, 782, 550, 900], fill=TABLE)
# mugs and plates on table
ell(d, [230, 706, 290, 724], fill=(240, 236, 224))
ell(d, [420, 708, 470, 722], fill=(240, 236, 224))
rr(d, [310, 700, 340, 724], 4, fill=BOWL_BLUE)
rr(d, [180, 704, 204, 722], 4, fill=(178, 96, 62))
# bread loaf
ell(d, [350, 706, 410, 724], fill=(198, 148, 88))

# ---- family seated at the table (relaxed, not in a line) ----
# adult 1 (left, leaning in, facing right)
person(d, 210, 700, 190, SKIN_A, HAIR_DARK, SHIRT_BLUE, "short", facing=1)
# adult 2 (right, facing left, long hair)
person(d, 500, 700, 190, SKIN_B, HAIR_BROWN, SHIRT_RUST, "long", facing=-1)
# child (between, slightly forward, small, facing the table)
person(d, 350, 720, 130, SKIN_C, HAIR_DARK, SHIRT_GREEN, "curls", facing=1)
# chairs (backs visible)
rr(d, [150, 700, 175, 860], 8, fill=(140, 98, 62))
rr(d, [540, 700, 565, 860], 8, fill=(140, 98, 62))

# ---- the robot: friendly household helper at the counter ----
# body: rounded, cream-white, apron-ish panel
rx, ry = 790, 660  # base
rr(d, [rx - 78, ry - 250, rx + 78, ry], 46, fill=ROBOT_BODY)
rr(d, [rx - 56, ry - 210, rx + 56, ry - 30], 24, fill=(196, 204, 208))
# head
rr(d, [rx - 58, ry - 340, rx + 58, ry - 240], 34, fill=ROBOT_BODY)
# face screen
rr(d, [rx - 44, ry - 326, rx + 44, ry - 258], 20, fill=(40, 52, 58))
ell(d, [rx - 26, ry - 306, rx - 10, ry - 290], fill=(140, 220, 200))
ell(d, [rx + 10, ry - 306, rx + 26, ry - 290], fill=(140, 220, 200))
d.arc([rx - 18, ry - 292, rx + 18, ry - 272], 20, 160, fill=(140, 220, 200), width=4)
# little antenna with warm light
d.line([(rx, ry - 340), (rx, ry - 372)], fill=ROBOT_DARK, width=5)
ell(d, [rx - 9, ry - 384, rx + 9, ry - 366], fill=ROBOT_ACCENT)
# arm reaching to the counter, holding a half-peeled carrot
d.line([(rx - 70, ry - 190), (rx - 150, ry - 130)], fill=ROBOT_BODY, width=26)
ell(d, [rx - 168, ry - 148, rx - 132, ry - 112], fill=ROBOT_DARK)
# carrot in its hand (half-peeled: orange with pale strip)
poly(d, [(rx - 158, ry - 128), (rx - 96, ry - 122), (rx - 158, ry - 104)], fill=CARROT)
poly(d, [(rx - 128, ry - 126), (rx - 96, ry - 122), (rx - 128, ry - 108)], fill=(250, 214, 160))
d.line([(rx - 158, ry - 122), (rx - 176, ry - 136)], fill=(110, 150, 80), width=5)
# other arm down at its side
d.line([(rx + 70, ry - 190), (rx + 96, ry - 90)], fill=ROBOT_BODY, width=26)
ell(d, [rx + 78, ry - 108, rx + 114, ry - 72], fill=ROBOT_DARK)
# base / wheels peeking under the counter edge
ell(d, [rx - 60, ry - 12, rx + 60, ry + 10], fill=ROBOT_DARK)
# carrot peels on the counter (the observed detail, part 1)
for px, py in [(700, 508), (720, 512), (688, 514), (740, 506)]:
    poly(d, [(px, py), (px + 16, py + 2), (px + 6, py + 8)], fill=(250, 190, 120))
# a second whole carrot on the counter
poly(d, [(660, 500), (700, 496), (660, 512)], fill=CARROT)

# ---- dog bowl on the floor (the specific detail) ----
bx, by = 880, 930
ell(d, [bx - 70, by - 18, bx + 70, by + 22], fill=(60, 60, 64))
ell(d, [bx - 58, by - 30, bx + 58, by + 6], fill=BOWL_BLUE)
ell(d, [bx - 44, by - 26, bx + 44, by - 2], fill=(120, 84, 60))
# a few kibbles beside it
for kx, ky in [(bx - 96, by + 8), (bx + 92, by + 4), (bx + 104, by + 14)]:
    ell(d, [kx, ky, kx + 8, ky + 6], fill=(120, 84, 60))

# ---- laundry draped over the radiator (left wall, low) ----
d.rectangle([60, 830, 300, 940], fill=(200, 198, 190))
for lx in range(70, 300, 26):
    d.line([(lx, 830), (lx, 940)], fill=(170, 168, 160), width=3)
# cloth over the top
poly(d, [(60, 830), (300, 830), (290, 880), (70, 880)], fill=(150, 170, 190))
poly(d, [(70, 880), (290, 880), (280, 920), (80, 920)], fill=(130, 150, 172))

# ---- soft vignette + grain for a photographic feel ----
img = img.filter(ImageFilter.GaussianBlur(0.6))
vig = Image.new("L", (W, H), 0)
vd = ImageDraw.Draw(vig)
vd.ellipse([-220, -220, W + 220, H + 220], fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(160))
dark = Image.new("RGB", (W, H), (30, 18, 8))
img = Image.composite(img, Image.blend(img, dark, 0.28), vig)
# grain
px = img.load()
for _ in range(9000):
    x = random.randrange(W)
    y = random.randrange(H)
    v = random.randint(-8, 8)
    r, g, b = px[x, y]
    px[x, y] = (max(0, min(255, r + v)), max(0, min(255, g + v)), max(0, min(255, b + v)))

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
