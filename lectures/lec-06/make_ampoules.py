# -*- coding: utf-8 -*-
"""
Декоративная картинка для лекции 6: питон пытается заменить запаянную ампулу.

Пара к картинке лекции 5 (make_rack.py, питон ставит пробирку в штатив).
Список -- штатив с открытыми пробирками: любую можно заменить. Кортеж --
кассета с запаянными ампулами: прочитать можно любую, заменить нельзя.
Все пять гнёзд заняты, питон держит шестую ампулу над гнездом 3,
и в облачке ответ Python на такую попытку.

Цвета берутся из токенов темы (--s1 … --s8, --surface, --accent-danger)
и currentColor, поэтому картинка сама переключается вместе со светлой/тёмной
темой. Цвета глаз зафиксированы: это мультяшный персонаж, его собственный
контраст не должен зависеть от фона.

Запуск:  python make_ampoules.py
Пишет:   pics/py_ampoules.svg  и  components/FigAmpoules.vue
"""
from pathlib import Path

SAY = "t[3] = 6.9"           # первая строка облачка; SAY = "" убирает облачко
ERR = "TypeError"            # вторая строка, красным; ERR = "" -- без неё

W, H = 860, 340

GREEN      = "var(--s3)"      # тело питона
GREEN_DARK = "var(--s6)"      # узор на теле
TONGUE     = "var(--s8)"      # язык
SCLERA     = "#fdfdfb"        # белок глаза  (фиксированный)
PUPIL      = "#17301f"        # зрачок       (фиксированный)
LIQUIDS    = ["var(--s1)", "var(--s2)", "var(--s4)", "var(--s3)", "var(--s5)"]  # все гнёзда заняты
HELD       = "var(--s7)"      # раствор в ампуле, которую держит питон
DANGER     = "var(--accent-danger)"   # цвет строки ERR

# ---------------------------------------------------------------- геометрия
SLOTS = [120, 200, 280, 360, 440]     # оси гнёзд
HW = 15                               # полуширина ампулы
Y_TIP, Y_SH, Y_PLATE, Y_LIQ, Y_BOT = 102, 150, 160, 196, 255   # ампула в кассете
NW = 5                                # полуширина горлышка
X_L, X_R = 80, 480                    # края штатива
Y_BASE = 290
HELD_CX, HELD_DY = SLOTS[3], -92      # держимая ампула: над гнездом 3, приподнята


def bez(p0, p1, p2, p3, t):
    """Точка на кубической кривой Безье."""
    u = 1 - t
    return (u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
            u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1])


# тело: задняя часть (уходит за ампулу) и передняя (обвивает её спереди)
BACK = [((728, 268), (660, 318), (566, 296), (528, 226)),
        ((528, 226), (494, 164), (430, 84), (338, 94))]
FRONT = [((338, 94), (312, 116), (348, 140), (392, 124)),
         ((392, 124), (432, 110), (452, 82), (482, 62))]


def curve(segs):
    d = f"M {segs[0][0][0]} {segs[0][0][1]}"
    for _, c1, c2, p in segs:
        d += f" C {c1[0]} {c1[1]}, {c2[0]} {c2[1]}, {p[0]} {p[1]}"
    return d


def body(segs, width):
    return (f'<path d="{curve(segs)}" fill="none" stroke="{GREEN}" '
            f'stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>')


def scales(segs, ts, r=4.2, opacity=0.30):
    out = []
    for seg, tt in ts:
        p0, c1, c2, p3 = segs[seg]
        for t in tt:
            x, y = bez(p0, c1, c2, p3, t)
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" '
                       f'fill="{GREEN_DARK}" opacity="{opacity}"/>')
    return "\n  ".join(out)


def ampoule(cx, dy=0, liquid=None, opaque=False):
    """Запаянная ампула с осью cx, сдвинутая по вертикали на dy.

    opaque=True подкладывает под стекло цвет фона: ампула заслоняет то,
    что за ней (нужно для ампулы в руках питона, она висит перед гнездом 3)."""
    tip, sh, liq, bot = Y_TIP + dy, Y_SH + dy, Y_LIQ + dy, Y_BOT + dy
    neck = sh - 16                     # где плечо переходит в горлышко
    seal = neck - 18                   # где горлышко начинает сужаться к носику
    glass = (f"M {cx-HW} {sh} L {cx-HW} {bot} A {HW} {HW} 0 0 0 {cx+HW} {bot} "
             f"L {cx+HW} {sh} C {cx+HW} {sh-9} {cx+NW} {neck+7} {cx+NW} {neck} "
             f"L {cx+NW} {seal} Q {cx+NW} {tip+4} {cx} {tip} "
             f"Q {cx-NW} {tip+4} {cx-NW} {seal} L {cx-NW} {neck} "
             f"C {cx-NW} {neck+7} {cx-HW} {sh-9} {cx-HW} {sh} Z")
    out = []
    if opaque:
        out.append(f'<path d="{glass}" fill="var(--surface, #fcfcfb)"/>')
    out.append(f'<path d="{glass}" fill="currentColor" opacity="0.05"/>')
    if liquid:
        fill = (f"M {cx-HW} {liq} q {HW/2:.1f} -6 {HW:.0f} 0 t {HW:.0f} 0 "
                f"L {cx+HW} {bot} A {HW} {HW} 0 0 1 {cx-HW} {bot} Z")
        out.append(f'<path d="{fill}" fill="{liquid}" opacity="0.45"/>')
        out.append(f'<path d="{fill}" fill="none" stroke="{liquid}" stroke-width="2" opacity="0.6"/>')
    out.append(f'<path d="{glass}" fill="none" stroke="currentColor" stroke-width="2.5" '
               'stroke-linejoin="round" opacity="0.5"/>')
    # оплавленный носик: капля стекла на конце
    out.append(f'<circle cx="{cx}" cy="{tip+2.5}" r="3.2" fill="currentColor" opacity="0.45"/>')
    # блик
    out.append(f'<path d="M {cx-8} {sh+14} L {cx-8} {bot-30}" stroke="currentColor" '
               'stroke-width="3" stroke-linecap="round" opacity="0.14"/>')
    return "\n  ".join(out)


# ---------------------------------------------------------------- надпись
# Текст рисуется КОНТУРАМИ, а не элементом <text>: размер <text> зависит
# от того, какой шрифт нашёлся в системе, и надпись может не влезть в облачко.
def text_to_path(s, size, font="DejaVu Sans Mono"):
    """Возвращает (d, ширина, высота, смещение_базовой_линии) для строки."""
    from matplotlib.textpath import TextPath
    from matplotlib.font_manager import FontProperties
    tp = TextPath((0, 0), s, size=size, prop=FontProperties(family=font))
    v, c = tp.vertices, tp.codes
    out, i = [], 0
    while i < len(v):
        code = c[i]
        if code == 1:                                   # MOVETO
            out.append(f"M {v[i][0]:.1f} {-v[i][1]:.1f}"); i += 1
        elif code == 2:                                 # LINETO
            out.append(f"L {v[i][0]:.1f} {-v[i][1]:.1f}"); i += 1
        elif code == 3:                                 # CURVE3
            out.append(f"Q {v[i][0]:.1f} {-v[i][1]:.1f} {v[i+1][0]:.1f} {-v[i+1][1]:.1f}"); i += 2
        elif code == 4:                                 # CURVE4
            out.append(f"C {v[i][0]:.1f} {-v[i][1]:.1f} {v[i+1][0]:.1f} {-v[i+1][1]:.1f} "
                       f"{v[i+2][0]:.1f} {-v[i+2][1]:.1f}"); i += 3
        else:                                           # CLOSEPOLY
            out.append("Z"); i += 1
    x0, y0, x1, y1 = tp.get_extents().extents
    return " ".join(out), x1 - x0, y1 - y0, y0


# ------------------------------------------------------------------- сборка
p = ["@SVG@"]
# мягкая тень: фиксированный тёмный цвет, на тёмной теме она просто исчезает
p.append(f'  <ellipse cx="{(X_L+X_R)//2}" cy="{Y_BASE+18}" rx="215" ry="8" '
         'fill="#1a1a19" opacity="0.07"/>')

# --- 1. тело за ампулой --------------------------------------------------
p.append('  <!-- хвост -->')
p.append(f'  <path d="M 728 268 c 30 14 48 -4 36 -22 c -8 -11 -22 -8 -24 2" '
         f'fill="none" stroke="{GREEN}" stroke-width="15" stroke-linecap="round"/>')
p.append('  ' + body(BACK, 26))
p.append('  ' + scales(BACK, [(0, (0.2, 0.48, 0.76)), (1, (0.2, 0.48, 0.76))]))

# --- 2. кассета --------------------------------------------------------------
p.append('  <!-- кассета -->')
p.append(f'  <rect x="{X_L+6}" y="{Y_PLATE}" width="9" height="{Y_BASE-Y_PLATE}" '
         'fill="currentColor" opacity="0.32"/>')
p.append(f'  <rect x="{X_R-15}" y="{Y_PLATE}" width="9" height="{Y_BASE-Y_PLATE}" '
         'fill="currentColor" opacity="0.32"/>')
p.append(f'  <rect x="{X_L}" y="{Y_BASE}" width="{X_R-X_L}" height="16" rx="4" '
         'fill="currentColor" opacity="0.42"/>')
p.append(f'  <rect x="{X_L}" y="{Y_PLATE}" width="{X_R-X_L}" height="18" rx="4" '
         'fill="currentColor" opacity="0.42"/>')
for cx in SLOTS:
    p.append(f'  <ellipse cx="{cx}" cy="{Y_PLATE+9}" rx="{HW+4}" ry="5" '
             'fill="var(--surface, #fcfcfb)" opacity="0.9"/>')

# ампулы в гнёздах (все гнёзда заняты: кортеж не меняется)
p.append('  <!-- ампулы -->')
for cx, liquid in zip(SLOTS, LIQUIDS):
    if liquid:
        p.append('  ' + ampoule(cx, 0, liquid))

# номера гнёзд
p.append('  <!-- индексы -->')
for i, cx in enumerate(SLOTS):
    try:
        d, tw, th, ybot = text_to_path(str(i), 22)
        p.append(f'  <path transform="translate({cx - tw/2:.1f} {Y_BASE + 44:.1f})" d="{d}" '
                 'fill="currentColor" opacity="0.75"/>')
    except Exception:
        p.append(f'  <text x="{cx}" y="{Y_BASE + 44}" text-anchor="middle" '
                 'font-family="monospace" style="font-size:22px" fill="currentColor" '
                 f'opacity="0.75">{i}</text>')

# --- 3. ампула в кольце питона и тело перед ней ---------------------------
p.append('  <!-- ампула над гнездом 3 -->')
p.append('  ' + ampoule(HELD_CX, HELD_DY, HELD, opaque=True))
p.append('  <!-- виток вокруг ампулы -->')
p.append('  ' + body(FRONT, 26))
p.append('  ' + scales(FRONT, [(0, (0.3, 0.64)), (1, (0.3, 0.66))]))

# --- 4. голова --------------------------------------------------------------
hx, hy = 512, 44                       # центр головы
p.append('  <!-- голова -->')
p.append(f'  <ellipse cx="{hx}" cy="{hy}" rx="37" ry="29" fill="{GREEN}" '
         f'transform="rotate(-12 {hx} {hy})"/>')
p.append(f'  <ellipse cx="{hx-12}" cy="{hy-9}" rx="9" ry="10" fill="{SCLERA}"/>')
p.append(f'  <ellipse cx="{hx+17}" cy="{hy-5}" rx="9" ry="10" fill="{SCLERA}"/>')
p.append(f'  <circle cx="{hx-9.5}" cy="{hy-7.5}" r="4.6" fill="{PUPIL}"/>')
p.append(f'  <circle cx="{hx+19.5}" cy="{hy-3.5}" r="4.6" fill="{PUPIL}"/>')
p.append(f'  <circle cx="{hx-8}" cy="{hy-10}" r="1.7" fill="{SCLERA}"/>')
p.append(f'  <circle cx="{hx+21}" cy="{hy-6}" r="1.7" fill="{SCLERA}"/>')
p.append(f'  <circle cx="{hx-1}" cy="{hy+9}" r="1.8" fill="{PUPIL}" opacity="0.55"/>')
p.append(f'  <circle cx="{hx+9}" cy="{hy+10.5}" r="1.8" fill="{PUPIL}" opacity="0.55"/>')
p.append(f'  <path d="M {hx-4} {hy+18} q 9 7 18 1" fill="none" stroke="{PUPIL}" '
         'stroke-width="2.4" stroke-linecap="round" opacity="0.55"/>')
# язык
p.append(f'  <path d="M {hx+15} {hy+24} C {hx+32} {hy+40}, {hx+54} {hy+38}, {hx+66} {hy+28}" '
         f'fill="none" stroke="{TONGUE}" stroke-width="4" stroke-linecap="round"/>')
p.append(f'  <path d="M {hx+66} {hy+28} l 15 -3 M {hx+66} {hy+28} l 10 10" fill="none" '
         f'stroke="{TONGUE}" stroke-width="4" stroke-linecap="round"/>')

# --- 5. реплика: код и ответ Python --------------------------------------
if SAY:
    lines = [(SAY, "currentColor")] + ([(ERR, DANGER)] if ERR else [])
    shapes = []
    for txt, color in lines:
        try:
            d, tw, th, ybot = text_to_path(txt, 28)
        except Exception as e:                  # matplotlib не найден: рисуем <text>
            print("! контуры не получились (%s), надпись останется текстом" % e)
            d, tw, th, ybot = None, 16.9 * len(txt), 20, -20
        shapes.append((txt, color, d, tw, th, ybot))
    bx, by = 628, 8                        # левый верхний угол облачка
    padx, pady, gap = 26, 18, 12
    line_h = 30                            # шаг строк по базовой линии
    bw = max(sh[3] for sh in shapes) + 2 * padx
    bh = 2 * pady + line_h * len(shapes) - (line_h - 22) + (gap if len(shapes) > 1 else 0)
    W = int(bx + bw + 16)                  # холст растягиваем под облачко
    p.append('  <!-- реплика -->')
    p.append(f'  <path d="M {bx+2} {by+20} l -24 16 l 24 12 Z" '
             'fill="var(--surface, #fcfcfb)" stroke="currentColor" stroke-width="2" '
             'stroke-linejoin="round" opacity="0.9"/>')
    p.append(f'  <rect x="{bx}" y="{by}" width="{bw:.0f}" height="{bh:.0f}" rx="16" '
             'fill="var(--surface, #fcfcfb)" stroke="currentColor" stroke-width="2" '
             'opacity="0.9"/>')
    base = by + pady + 22                  # базовая линия первой строки
    for k, (txt, color, d, tw, th, ybot) in enumerate(shapes):
        tx, ty = bx + padx, base + k * (line_h + gap)
        if d:
            p.append(f'  <path transform="translate({tx:.1f} {ty:.1f})" d="{d}" '
                     f'fill="{color}"/>')
        else:
            p.append(f'  <text x="{tx:.0f}" y="{ty:.0f}" font-family="monospace" '
                     f'style="font-size:28px" fill="{color}">{txt}</text>')

p.append('</svg>')
p[0] = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
svg = "\n".join(p) + "\n"

root = Path(__file__).resolve().parent
(root / "pics").mkdir(exist_ok=True)
(root / "components").mkdir(exist_ok=True)
(root / "pics" / "py_ampoules.svg").write_text(svg, encoding="utf-8")
(root / "components" / "FigAmpoules.vue").write_text(
    "<!-- Сгенерировано make_ampoules.py: не редактировать вручную -->\n"
    "<template>\n" + svg + "</template>\n", encoding="utf-8")
print("pics/py_ampoules.svg  +  components/FigAmpoules.vue")
