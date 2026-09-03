# -*- coding: utf-8 -*-
"""
make_hello.py — схема «анатомия первой программы» для слайда
«Простейшая программа на Python».

Рисуется прямо в SVG: цвета — currentColor и var(--sN), поэтому картинка
переключается вместе с темой слайдов, как и графики из figtheme.
Символы позиционируются через textLength/lengthAdjust — положение
не зависит от того, какой моноширинный шрифт окажется в системе.
"""
from pathlib import Path

CODE = "print('Привет Мир!')"
PITCH = 26          # ширина знакоместа, px
FS = 34             # кегль кода
X0 = 70             # левый край кода
Y_CODE = 132        # базовая линия кода
W, H = 800, 366

MONO = "'JetBrains Mono', 'Cascadia Mono', Consolas, 'DejaVu Sans Mono', monospace"
SANS = "Inter, 'Segoe UI', Roboto, Arial, sans-serif"


def cx(i):
    """Центр i-го знакоместа."""
    return X0 + PITCH * i + PITCH / 2


def brace_up(i0, i1, y, color):
    """Скобка-подчёркивание под символами с i0 по i1 включительно."""
    x0, x1 = X0 + PITCH * i0 + 3, X0 + PITCH * (i1 + 1) - 3
    xm = (x0 + x1) / 2
    return (f'<path d="M {x0} {y} v 8 H {x1} v -8" fill="none" '
            f'stroke="{color}" stroke-width="2" stroke-linejoin="round"/>'
            f'<path d="M {xm} {y + 8} v 12" stroke="{color}" stroke-width="2"/>')


def brace_down(i0, i1, y, color):
    """Скобка над символами (усики вниз)."""
    x0, x1 = X0 + PITCH * i0 + 3, X0 + PITCH * (i1 + 1) - 3
    xm = (x0 + x1) / 2
    return (f'<path d="M {x0} {y} v -8 H {x1} v 8" fill="none" '
            f'stroke="{color}" stroke-width="2" stroke-linejoin="round"/>'
            f'<path d="M {xm} {y - 8} v -12" stroke="{color}" stroke-width="2"/>')


def tick_down(i, y, color):
    """Вертикальный штрих от символа вниз."""
    return f'<path d="M {cx(i)} {y} v 26" stroke="{color}" stroke-width="2"/>'


def label(x, y, text, color, anchor="middle", size=17, weight=600):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{SANS}" '
            f'font-size="{size}" font-weight="{weight}" fill="{color}">{text}</text>')


parts = []

# ── код ──────────────────────────────────────────────────────────────────────
parts.append(
    f'<text x="{X0}" y="{Y_CODE}" font-family="{MONO}" font-size="{FS}" '
    f'fill="currentColor" xml:space="preserve" '
    f'textLength="{PITCH * len(CODE)}" lengthAdjust="spacing">{CODE}</text>')

# ── сверху: имя функции и аргумент ───────────────────────────────────────────
Y_UP = Y_CODE - FS - 6
parts.append(brace_down(0, 4, Y_UP, "var(--s1)"))
parts.append(label((cx(0) + cx(4)) / 2, Y_UP - 30, "имя функции", "var(--s1)"))

parts.append(brace_down(7, 17, Y_UP, "var(--s3)"))
parts.append(label((cx(7) + cx(17)) / 2, Y_UP - 30,
                   "аргумент — то, что выводим", "var(--s3)"))

# ── снизу: скобки и кавычки, точками-маркерами без линий ─────────────────────
# Соединительные линии здесь пересекались бы, поэтому вместо них — точка
# под символом и такая же точка перед подписью, как в легенде.
Y_DOT = Y_CODE + 22
R = 5

for i in (5, 19):
    parts.append(f'<circle cx="{cx(i)}" cy="{Y_DOT}" r="{R}" fill="var(--s2)"/>')
for i in (6, 18):
    parts.append(f'<circle cx="{cx(i)}" cy="{Y_DOT}" r="{R}" fill="var(--s5)"/>')

LEG_X = X0 + 4
for k, (color, text) in enumerate((
        ("var(--s2)", "круглые скобки — вызываем функцию"),
        ("var(--s5)", "кавычки — внутри текст, а не имя переменной"))):
    y = Y_DOT + 44 + k * 32
    parts.append(f'<circle cx="{LEG_X}" cy="{y - 5}" r="{R}" fill="{color}"/>')
    parts.append(label(LEG_X + 16, y, text, color, anchor="start", size=17))

# ── результат ────────────────────────────────────────────────────────────────
Y_RES = 300
parts.append(f'<path d="M {X0 + 10} {Y_RES - 34} v 18" stroke="currentColor" '
             f'stroke-width="2" opacity="0.45"/>')
parts.append(f'<path d="M {X0 + 4} {Y_RES - 22} l 6 8 l 6 -8" fill="none" '
             f'stroke="currentColor" stroke-width="2" opacity="0.45" '
             f'stroke-linecap="round" stroke-linejoin="round"/>')
parts.append(f'<rect x="{X0 - 6}" y="{Y_RES - 8}" width="330" height="46" rx="8" '
             f'fill="currentColor" opacity="0.07"/>')
parts.append(f'<text x="{X0 + 12}" y="{Y_RES + 22}" font-family="{MONO}" '
             f'font-size="24" fill="currentColor">Привет Мир!</text>')
parts.append(label(X0 + 350, Y_RES + 21, "— то, что увидим в консоли",
                   "currentColor", anchor="start", size=16, weight=400))

svg = (f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">\n  '
       + "\n  ".join(parts) + "\n</svg>\n")

Path("pics/hello_anatomy.svg").write_text(svg, encoding="utf-8")
Path("components/FigHello.vue").write_text(
    "<!-- Сгенерировано make_hello.py — не редактировать вручную -->\n"
    f"<template>\n{svg}</template>\n", encoding="utf-8")
print("готово:", len(svg), "байт")
