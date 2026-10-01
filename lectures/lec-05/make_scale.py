# -*- coding: utf-8 -*-
"""
Схема к слайду «Шаг шкалы растёт вместе с числом».

Показывает главный механизм плавающей точки: между соседними степенями двойки
помещается ОДИНАКОВОЕ количество представимых чисел, а сам промежуток вдвое
длиннее. Отсюда: чем больше число, тем крупнее шаг шкалы.

Цвета — из токенов темы, поэтому картинка переключается вместе со светлой/тёмной.
Подписи переведены в контуры (matplotlib.textpath), чтобы размер не зависел
ни от установленных шрифтов, ни от стилей темы.

Запуск: python make_scale.py
Пишет:  pics/float_scale.svg  и  components/FigScale.vue
"""
from pathlib import Path

W, H = 820, 188
Y = 82                       # ось
X0, X1 = 46, 786
N_TICKS = 16                 # «представимых чисел» в каждом промежутке
ZONES = [(1, 2), (2, 4), (4, 8)]
COLORS = ["var(--s1)", "var(--s3)", "var(--s2)"]


def text_path(s, size, font="DejaVu Sans"):
    from matplotlib.textpath import TextPath
    from matplotlib.font_manager import FontProperties
    tp = TextPath((0, 0), s, size=size, prop=FontProperties(family=font))
    v, c = tp.vertices, tp.codes
    out, i = [], 0
    while i < len(v):
        code = c[i]
        if code == 1:
            out.append(f"M {v[i][0]:.1f} {-v[i][1]:.1f}"); i += 1
        elif code == 2:
            out.append(f"L {v[i][0]:.1f} {-v[i][1]:.1f}"); i += 1
        elif code == 3:
            out.append(f"Q {v[i][0]:.1f} {-v[i][1]:.1f} {v[i+1][0]:.1f} {-v[i+1][1]:.1f}"); i += 2
        elif code == 4:
            out.append(f"C {v[i][0]:.1f} {-v[i][1]:.1f} {v[i+1][0]:.1f} {-v[i+1][1]:.1f} "
                       f"{v[i+2][0]:.1f} {-v[i+2][1]:.1f}"); i += 3
        else:
            out.append("Z"); i += 1
    x0, y0, x1, y1 = tp.get_extents().extents
    return " ".join(out), x1 - x0, y1 - y0


def label(s, cx, y, size=19, color="currentColor", anchor="middle"):
    d, w, h = text_path(s, size)
    x = cx - w / 2 if anchor == "middle" else cx
    return f'  <path transform="translate({x:.1f} {y:.1f})" d="{d}" fill="{color}"/>'


# ширины зон: 1..2 -> 1, 2..4 -> 2, 4..8 -> 4  (в единицах числовой оси)
total = sum(b - a for a, b in ZONES)
p = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">']

x = X0
bounds = [X0]
for (a, b), col in zip(ZONES, COLORS):
    w = (X1 - X0) * (b - a) / total
    # подложка зоны
    p.append(f'  <rect x="{x:.1f}" y="{Y-46}" width="{w:.1f}" height="60" rx="6" '
             f'fill="{col}" opacity="0.09"/>')
    # засечки: одинаковое количество на зону
    for k in range(N_TICKS):
        tx = x + w * k / N_TICKS
        p.append(f'  <path d="M {tx:.1f} {Y-30} V {Y}" stroke="{col}" stroke-width="2" '
                 'stroke-linecap="round"/>')
    # количество чисел в зоне
    p.append(label(f"{N_TICKS} чисел", x + w / 2, Y - 58, 17, col))
    x += w
    bounds.append(x)

# ось
p.append(f'  <path d="M {X0-14} {Y} H {X1+22}" stroke="currentColor" stroke-width="2.5"/>')
p.append(f'  <path d="M {X1+14} {Y-6} l 10 6 l -10 6" fill="none" stroke="currentColor" '
         'stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>')

# подписи границ
for xb, name in zip(bounds, ["1", "2", "4", "8"]):
    p.append(f'  <path d="M {xb:.1f} {Y} V {Y+9}" stroke="currentColor" stroke-width="2.5"/>')
    p.append(label(name, xb, Y + 32))

# ширина шага под каждой зоной
for i, ((a, b), col) in enumerate(zip(ZONES, COLORS)):
    xa, xb = bounds[i], bounds[i + 1]
    yy = Y + 62
    p.append(f'  <path d="M {xa:.1f} {yy} H {xb:.1f}" stroke="{col}" stroke-width="2" '
             'opacity="0.75"/>')
    p.append(f'  <path d="M {xa:.1f} {yy-5} V {yy+5} M {xb:.1f} {yy-5} V {yy+5}" '
             f'stroke="{col}" stroke-width="2" opacity="0.75"/>')
    step = ["длина 1", "длина 2", "длина 4"][i]
    p.append(label(step, (xa + xb) / 2, yy + 26, 17, col))

p.append('</svg>')
svg = "\n".join(p) + "\n"

root = Path(__file__).resolve().parent
(root / "pics").mkdir(exist_ok=True)
(root / "components").mkdir(exist_ok=True)
(root / "pics" / "float_scale.svg").write_text(svg, encoding="utf-8")
(root / "components" / "FigScale.vue").write_text(
    "<!-- Сгенерировано make_scale.py — не редактировать вручную -->\n"
    "<template>\n" + svg + "</template>\n", encoding="utf-8")
print("pics/float_scale.svg + components/FigScale.vue,",
      len(svg.encode()) // 1024, "КБ")
