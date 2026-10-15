# -*- coding: utf-8 -*-
"""
Декоративная картинка для лекции 7: питон берёт с полки банку по этикетке.

Третья в серии после make_rack.py (лекция 5) и make_ampoules.py (лекция 6).
Список -- штатив: пробирки стоят в пронумерованных гнёздах. Кортеж -- кассета
с запаянными ампулами. Словарь -- полка с банками реактивов: номеров нет,
банку находят по этикетке, то есть по ключу. Питон снимает банку CuSO4,
в облачке обращение по ключу.

Цвета берутся из токенов темы (--s1 … --s8, --surface) и currentColor,
поэтому картинка сама переключается вместе со светлой/тёмной темой. Цвета
глаз зафиксированы: это мультяшный персонаж, его собственный контраст
не должен зависеть от фона. Текст этикеток и облачка нарисован контурами.

Запуск:  python make_jars.py
Пишет:   pics/py_jars.svg  и  components/FigJars.vue
"""
from pathlib import Path

SAY = "shelf['CuSO4']"       # первая строка облачка; SAY = "" убирает облачко
ERR = ""                     # вторая строка, красным; ERR = "" -- без неё

W, H = 860, 340

GREEN      = "var(--s3)"      # тело питона
GREEN_DARK = "var(--s6)"      # узор на теле
TONGUE     = "var(--s8)"      # язык
SCLERA     = "#fdfdfb"        # белок глаза  (фиксированный)
PUPIL      = "#17301f"        # зрачок       (фиксированный)
# банки на полке: (этикетка, цвет содержимого); None -- место пустое, банку держит питон
JARS       = [("NaCl", "var(--s2)"), ("KBr", "var(--s4)"), ("NaOH", "var(--s5)"),
              None, ("HCl", "var(--s3)")]
HELD       = ("CuSO4", "var(--s1)")   # банка в кольце питона: медный купорос -- синий
DANGER     = "var(--accent-danger)"   # цвет строки ERR

# ---------------------------------------------------------------- геометрия
SLOTS = [120, 200, 280, 360, 440]     # оси мест на полке
HW = 26                               # полуширина банки
NW = 17                               # полуширина горлышка
Y_CAP, Y_NECK, Y_SH, Y_LIQ, Y_BOT = 160, 172, 186, 214, 288   # банка на полке
X_L, X_R = 80, 480                    # края полки
Y_BASE = 290
HELD_CX, HELD_DY = SLOTS[3], -110     # держимая банка: над местом 3, приподнята


def bez(p0, p1, p2, p3, t):
    """Точка на кубической кривой Безье."""
    u = 1 - t
    return (u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
            u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1])


# тело: задняя часть (уходит за банку) и передняя (обвивает её спереди)
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


def jar(cx, dy=0, liquid=None, opaque=False):
    """Банка с осью cx, сдвинутая по вертикали на dy (этикетка -- отдельно, label()).

    opaque=True подкладывает под стекло цвет фона: банка заслоняет то,
    что за ней (нужно для банки в руках питона)."""
    cap, neck, sh, liq, bot = Y_CAP + dy, Y_NECK + dy, Y_SH + dy, Y_LIQ + dy, Y_BOT + dy
    r = 9                                  # скругление дна
    glass = (f"M {cx-NW} {neck} L {cx-NW} {sh-4} Q {cx-HW} {sh-2} {cx-HW} {sh+8} "
             f"L {cx-HW} {bot-r} Q {cx-HW} {bot} {cx-HW+r} {bot} "
             f"L {cx+HW-r} {bot} Q {cx+HW} {bot} {cx+HW} {bot-r} "
             f"L {cx+HW} {sh+8} Q {cx+HW} {sh-2} {cx+NW} {sh-4} L {cx+NW} {neck} Z")
    out = []
    if opaque:
        out.append(f'<path d="{glass}" fill="var(--surface, #fcfcfb)"/>')
    out.append(f'<path d="{glass}" fill="currentColor" opacity="0.05"/>')
    if liquid:
        fill = (f"M {cx-HW} {liq} q {HW/2:.1f} -5 {HW:.0f} 0 t {HW:.0f} 0 "
                f"L {cx+HW} {bot-r} Q {cx+HW} {bot} {cx+HW-r} {bot} "
                f"L {cx-HW+r} {bot} Q {cx-HW} {bot} {cx-HW} {bot-r} Z")
        out.append(f'<path d="{fill}" fill="{liquid}" opacity="0.45"/>')
        out.append(f'<path d="{fill}" fill="none" stroke="{liquid}" stroke-width="2" opacity="0.6"/>')
    out.append(f'<path d="{glass}" fill="none" stroke="currentColor" stroke-width="2.5" '
               'stroke-linejoin="round" opacity="0.5"/>')
    # крышка
    out.append(f'<rect x="{cx-NW-4}" y="{cap}" width="{2*NW+8}" height="{neck-cap+2}" rx="3" '
               'fill="currentColor" opacity="0.42"/>')
    # блик
    out.append(f'<path d="M {cx-HW+7} {sh+14} L {cx-HW+7} {bot-16}" stroke="currentColor" '
               'stroke-width="3" stroke-linecap="round" opacity="0.14"/>')
    return "\n  ".join(out)


def label(cx, dy, text, low=False):
    """Этикетка на банке: белая плашка с надписью, надпись -- контурами.

    low=True опускает этикетку к дну: у банки в руках питона середину
    закрывает виток тела."""
    y0 = (Y_BOT + dy - 32) if low else (Y_LIQ + dy + 18)   # верх этикетки
    lw, lh = 2 * HW - 8, 24
    out = [f'<rect x="{cx-lw/2:.1f}" y="{y0}" width="{lw}" height="{lh}" rx="3" '
           'fill="var(--surface, #fcfcfb)" stroke="currentColor" stroke-width="1.2" opacity="0.95"/>']
    try:
        d, tw, th, ybot = text_to_path(text, 12.5)
        out.append(f'<path transform="translate({cx - tw/2:.1f} {y0 + lh/2 + th/2 + ybot:.1f})" '
                   f'd="{d}" fill="currentColor"/>')
    except Exception:
        out.append(f'<text x="{cx}" y="{y0 + 17}" text-anchor="middle" font-family="monospace" '
                   f'style="font-size:12.5px" fill="currentColor">{text}</text>')
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

# --- 1. тело за банкой --------------------------------------------------
p.append('  <!-- хвост -->')
p.append(f'  <path d="M 728 268 c 30 14 48 -4 36 -22 c -8 -11 -22 -8 -24 2" '
         f'fill="none" stroke="{GREEN}" stroke-width="15" stroke-linecap="round"/>')
p.append('  ' + body(BACK, 26))
p.append('  ' + scales(BACK, [(0, (0.2, 0.48, 0.76)), (1, (0.2, 0.48, 0.76))]))

# --- 2. полка ----------------------------------------------------------------
p.append('  <!-- полка -->')
p.append(f'  <rect x="{X_L}" y="{Y_BASE}" width="{X_R-X_L}" height="14" rx="3" '
         'fill="currentColor" opacity="0.42"/>')
for xb in (X_L + 22, X_R - 34):            # кронштейны
    p.append(f'  <path d="M {xb} {Y_BASE+14} l 0 22 l 12 0 Z" fill="currentColor" opacity="0.3"/>')

# банки на полке (место 3 пустое: его банку держит питон)
p.append('  <!-- банки -->')
for cx, item in zip(SLOTS, JARS):
    if item:
        name, liquid = item
        p.append('  ' + jar(cx, 0, liquid))
        p.append('  ' + label(cx, 0, name))

# --- 3. банка в кольце питона и тело перед ней ---------------------------
p.append('  <!-- банка над местом 3 -->')
p.append('  ' + jar(HELD_CX, HELD_DY, HELD[1], opaque=True))
p.append('  <!-- виток вокруг банки -->')
p.append('  ' + body(FRONT, 26))
p.append('  ' + scales(FRONT, [(0, (0.3, 0.64)), (1, (0.3, 0.66))]))
p.append('  <!-- этикетка банки в руках: поверх витка, у дна -->')
p.append('  ' + label(HELD_CX, HELD_DY, HELD[0], low=True))

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
(root / "pics" / "py_jars.svg").write_text(svg, encoding="utf-8")
(root / "components" / "FigJars.vue").write_text(
    "<!-- Сгенерировано make_jars.py: не редактировать вручную -->\n"
    "<template>\n" + svg + "</template>\n", encoding="utf-8")
print("pics/py_jars.svg  +  components/FigJars.vue")
