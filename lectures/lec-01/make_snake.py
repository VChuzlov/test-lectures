# -*- coding: utf-8 -*-
"""
Декоративная картинка для лекции: питон, обвивший коническую колбу.
Без информационной нагрузки — просто «глазу отдохнуть».

Цвета берутся из токенов темы (--s1, --s3, --s6, --s8, --surface) и currentColor,
поэтому картинка сама переключается вместе со светлой/тёмной темой.
Локальные цвета глаз намеренно зафиксированы: это мультяшный персонаж,
его собственный контраст не должен зависеть от фона.

Запуск:  python make_snake.py
Пишет:   pics/py_flask.svg  и  components/FigSnake.vue
"""
from pathlib import Path

SAY = "Привет Мир!"      # текст в облачке; поставьте SAY = "" — облачко исчезнет

W, H = 780, 440
SANS = "Inter, 'Segoe UI', Roboto, Arial, sans-serif"
MONO = "'JetBrains Mono', 'Cascadia Mono', Consolas, 'DejaVu Sans Mono', monospace"

GREEN      = "var(--s3)"          # тело питона
GREEN_DARK = "var(--s6)"          # узор на теле
LIQ        = "var(--s1)"          # раствор в колбе
TONGUE     = "var(--s8)"          # язык
SCLERA     = "#fdfdfb"            # белок глаза  (фиксированный)
PUPIL      = "#17301f"            # зрачок       (фиксированный)

# ---------------------------------------------------------------- геометрия
CX = 270                      # ось колбы
Y_RIM, Y_NECK, Y_BOT = 132, 212, 394
HW_NECK, HW_BOT = 24, 82
Y_LIQ = 322


def hw(y):
    """Полуширина конуса на высоте y."""
    return HW_NECK + (y - Y_NECK) * (HW_BOT - HW_NECK) / (Y_BOT - 10 - Y_NECK)


def bez(p0, p1, p2, p3, t):
    """Точка на кубической кривой Безье."""
    u = 1 - t
    return (u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
            u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1])


# тело: задняя часть (уходит за колбу) и передняя (пересекает горлышко)
BACK = [((470, 336), (424, 358), (366, 342), (336, 306)),
        ((336, 306), (302, 268), (278, 228), (228, 198))]
FRONT = [((228, 198), (212, 168), (254, 152), (292, 164)),
         ((292, 164), (330, 176), (342, 140), (362, 116))]


def curve(segs):
    d = f"M {segs[0][0][0]} {segs[0][0][1]}"
    for _, c1, c2, p in segs:
        d += f" C {c1[0]} {c1[1]}, {c2[0]} {c2[1]}, {p[0]} {p[1]}"
    return d


def body(segs, width, opacity=1.0):
    return (f'<path d="{curve(segs)}" fill="none" stroke="{GREEN}" '
            f'stroke-width="{width}" stroke-linecap="round" '
            f'stroke-linejoin="round" opacity="{opacity}"/>')


def scales(segs, ts, r=4.2, opacity=0.30):
    out = []
    for seg, tt in ts:
        p0, c1, c2, p3 = segs[seg]
        for t in tt:
            x, y = bez(p0, c1, c2, p3, t)
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" '
                       f'fill="{GREEN_DARK}" opacity="{opacity}"/>')
    return "\n  ".join(out)



# ---------------------------------------------------------------- надпись
# Текст в облачке рисуется КОНТУРАМИ, а не элементом <text>. Причина: размер
# <text> зависит от того, какой шрифт нашёлся в системе и не переопределил ли
# кто-то font-size в CSS темы, — из-за этого надпись может не влезть в облачко.
# Контуры выглядят одинаково везде, а облачко подгоняется под них по факту.
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
p = []
p.append("@SVG@")
# мягкая тень: намеренно фиксированный тёмный цвет — на тёмной теме
# она совпадает с фоном и просто исчезает, а не превращается в свечение
p.append('  <ellipse cx="282" cy="400" rx="128" ry="9" fill="#1a1a19" opacity="0.07"/>')

# --- 1. тело за колбой ------------------------------------------------------
p.append('  <!-- хвост -->')
p.append('  <path d="M 470 336 c 26 10 40 -6 30 -20 c -6 -9 -18 -8 -21 1" '
         f'fill="none" stroke="{GREEN}" stroke-width="15" stroke-linecap="round"/>')
p.append('  ' + body(BACK, 26))
p.append('  ' + scales(BACK, [(0, (0.18, 0.46, 0.74)), (1, (0.16, 0.44, 0.72))]))

# --- 2. колба ---------------------------------------------------------------
flask = (f"M {CX-HW_NECK} {Y_RIM+14} L {CX-HW_NECK} {Y_NECK} "
         f"L {CX-HW_BOT} {Y_BOT-10} Q {CX-HW_BOT-3} {Y_BOT} {CX-HW_BOT+7} {Y_BOT} "
         f"L {CX+HW_BOT-7} {Y_BOT} Q {CX+HW_BOT+3} {Y_BOT} {CX+HW_BOT} {Y_BOT-10} "
         f"L {CX+HW_NECK} {Y_NECK} L {CX+HW_NECK} {Y_RIM+14} Z")
p.append('  <!-- колба -->')
p.append(f'  <path d="{flask}" fill="currentColor" opacity="0.045"/>')

# раствор
hwl = hw(Y_LIQ)
seg = 2 * hwl / 3
liq = (f"M {CX-hwl:.1f} {Y_LIQ} q {seg/2:.1f} -9 {seg:.1f} 0 t {seg:.1f} 0 t {seg:.1f} 0 "
       f"L {CX+HW_BOT} {Y_BOT-10} Q {CX+HW_BOT+3} {Y_BOT} {CX+HW_BOT-7} {Y_BOT} "
       f"L {CX-HW_BOT+7} {Y_BOT} Q {CX-HW_BOT-3} {Y_BOT} {CX-HW_BOT} {Y_BOT-10} Z")
p.append(f'  <path d="{liq}" fill="{LIQ}" opacity="0.40"/>')
p.append(f'  <path d="{liq}" fill="none" stroke="{LIQ}" stroke-width="2" opacity="0.55"/>')

# пузырьки
for x, y, r in [(238, 300, 6), (262, 272, 4.5), (248, 246, 3.4),
                (286, 288, 3.2), (274, 336, 5), (232, 352, 4), (296, 330, 3)]:
    p.append(f'  <circle cx="{x}" cy="{y}" r="{r}" fill="none" '
             f'stroke="{LIQ}" stroke-width="2" opacity="0.5"/>')

# стекло и венчик
p.append(f'  <path d="{flask}" fill="none" stroke="currentColor" stroke-width="3" '
         'stroke-linejoin="round" opacity="0.5"/>')
p.append(f'  <rect x="{CX-36}" y="{Y_RIM}" width="72" height="14" rx="7" '
         'fill="currentColor" opacity="0.38"/>')
# блик на стекле
p.append('  <path d="M 246 252 L 228 316" stroke="currentColor" stroke-width="4" '
         'stroke-linecap="round" opacity="0.16"/>')

# --- 3. тело перед колбой ---------------------------------------------------
p.append('  <!-- виток вокруг горлышка -->')
p.append('  ' + body(FRONT, 26))
p.append('  ' + scales(FRONT, [(0, (0.28, 0.62)), (1, (0.3, 0.66))]))

# --- 4. голова --------------------------------------------------------------
p.append('  <!-- голова -->')
p.append(f'  <ellipse cx="392" cy="92" rx="37" ry="29" fill="{GREEN}" '
         'transform="rotate(-12 392 92)"/>')
p.append(f'  <ellipse cx="380" cy="83" rx="9" ry="10" fill="{SCLERA}"/>')
p.append(f'  <ellipse cx="409" cy="87" rx="9" ry="10" fill="{SCLERA}"/>')
p.append(f'  <circle cx="382.5" cy="84.5" r="4.6" fill="{PUPIL}"/>')
p.append(f'  <circle cx="411.5" cy="88.5" r="4.6" fill="{PUPIL}"/>')
p.append(f'  <circle cx="384" cy="82" r="1.7" fill="{SCLERA}"/>')
p.append(f'  <circle cx="413" cy="86" r="1.7" fill="{SCLERA}"/>')
p.append(f'  <circle cx="391" cy="101" r="1.8" fill="{PUPIL}" opacity="0.55"/>')
p.append(f'  <circle cx="401" cy="102.5" r="1.8" fill="{PUPIL}" opacity="0.55"/>')
p.append('  <path d="M 388 110 q 9 7 18 1" fill="none" stroke="' + PUPIL +
         '" stroke-width="2.4" stroke-linecap="round" opacity="0.55"/>')
# язык
p.append(f'  <path d="M 407 116 C 424 132, 446 130, 458 120" fill="none" '
         f'stroke="{TONGUE}" stroke-width="4" stroke-linecap="round"/>')
p.append(f'  <path d="M 458 120 l 15 -3 M 458 120 l 10 10" fill="none" '
         f'stroke="{TONGUE}" stroke-width="4" stroke-linecap="round"/>')

# --- 5. реплика -------------------------------------------------------------
if SAY:
    try:
        d, tw, th, ybot = text_to_path(SAY, 30)
    except Exception as e:                      # matplotlib не найден — рисуем <text>
        print("! контуры не получились (%s), надпись останется текстом" % e)
        d, tw, th, ybot = None, 18.1 * len(SAY), 22, -22
    bx, by = 496, 24                       # левый верхний угол облачка
    padx, pady = 30, 24
    bw, bh = tw + 2 * padx, max(th + 2 * pady, 72)
    tx = bx + padx                          # текст прижат к левому краю + отступ
    ty = by + bh / 2 - (th / 2 + ybot)      # базовая линия: по центру по вертикали
    W = int(bx + bw + 26)                   # холст растягиваем под облачко
    p.append('  <!-- реплика -->')
    p.append('  <path d="M 512 %d l -14 26 l 34 -14 Z" fill="var(--surface, #fcfcfb)" '
             'stroke="currentColor" stroke-width="2" stroke-linejoin="round" '
             'opacity="0.9"/>' % (by + bh - 4))
    p.append(f'  <rect x="{bx}" y="{by}" width="{bw:.0f}" height="{bh:.0f}" rx="16" '
             'fill="var(--surface, #fcfcfb)" stroke="currentColor" stroke-width="2" '
             'opacity="0.9"/>')
    if d:
        p.append(f'  <path transform="translate({tx:.1f} {ty:.1f})" d="{d}" '
                 'fill="currentColor"/>')
    else:
        p.append(f'  <text x="{tx:.0f}" y="{ty:.0f}" font-family="{MONO}" '
                 f'style="font-size:30px" textLength="{tw:.0f}" '
                 f'lengthAdjust="spacingAndGlyphs" fill="currentColor">{SAY}</text>')

p.append('</svg>')
p[0] = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
svg = "\n".join(p) + "\n"

root = Path(__file__).resolve().parent
(root / "pics").mkdir(exist_ok=True)
(root / "components").mkdir(exist_ok=True)
(root / "pics" / "py_flask.svg").write_text(svg, encoding="utf-8")
(root / "components" / "FigSnake.vue").write_text(
    "<!-- Сгенерировано make_snake.py — не редактировать вручную -->\n"
    "<template>\n" + svg + "</template>\n", encoding="utf-8")
print("pics/py_flask.svg  +  components/FigSnake.vue")
