"""
figtheme.py — графики matplotlib, которые сами подстраиваются под светлую и тёмную тему.

ИДЕЯ
----
matplotlib рисует график служебными цветами-маркерами, а после сохранения SVG
эти цвета заменяются на CSS-значения:

    обвязка графика (оси, текст, рамки, сетка) -> currentColor
    линии/точки данных (серия 1..8)            -> var(--s1) ... var(--s8)

В итоге ОДИН файл графика корректно выглядит и на светлом, и на тёмном фоне
и переключается мгновенно вместе с темой слайдов — без второй копии картинки.

ВАЖНО: `currentColor` и `var(--s1)` работают только для ИНЛАЙНОВОГО SVG в DOM.
Через `<img src="fig.svg">` они не работают. Поэтому save_adaptive() дополнительно
кладёт готовый Vue-компонент в components/ — Slidev подхватывает его автоматически.

ИСПОЛЬЗОВАНИЕ
-------------
    import numpy as np, matplotlib.pyplot as plt
    from figtheme import use_adaptive, save_adaptive

    use_adaptive()
    fig, ax = plt.subplots()
    ax.plot(T, cp, label='1-гексен')
    ax.set_xlabel('T, K'); ax.set_ylabel('Cp, Дж/(моль·К)'); ax.legend()
    save_adaptive(fig, 'pics/cp')      # -> pics/cp.svg и components/FigCp.vue

В слайде:

    <FigCp class="w-[560px] mx-auto" />

Переменные --s1..--s8 объявлены в style.css (см. комплект).
"""
from __future__ import annotations

import re
from pathlib import Path

import matplotlib as mpl

# ── служебные цвета-маркеры (реальными данными их не используем) ──────────────
_FG = "#010203"      # оси, текст, рамки, штрихи  -> currentColor
_GRID = "#040506"    # сетка                      -> currentColor + opacity
_SERIES = [f"#1000{i:02d}" for i in range(1, 9)]   # #100001 ... #100008 -> var(--sN)

# ── палитра «для человека»: используется в запасном режиме save_pair() ────────
# Проверена валидатором на светлой (#fcfcfb) и тёмной (#1a1a19) подложке:
# различима при протанопии / дейтеранопии / тританопии.
PALETTE_LIGHT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]
PALETTE_DARK = ["#3987e5", "#d95926", "#199e70", "#c98500", "#d55181", "#008300"]

FONT_STACK = "Inter, 'Segoe UI', Roboto, Arial, sans-serif"


def use_adaptive() -> None:
    """Включить стиль, пригодный для адаптивного экспорта.

    Раскладку текста matplotlib считает своим шрифтом (DejaVu Sans), а в SVG
    подставляется шрифт страницы; для подписей осей расхождение метрик
    несущественно.
    """
    mpl.rcParams.update({
        "svg.fonttype": "none",          # текст остаётся <text> -> наследует цвет и шрифт
        "savefig.transparent": True,
        "figure.facecolor": "none",
        "axes.facecolor": "none",
        "savefig.facecolor": "none",
        "font.size": 12,
        "axes.edgecolor": _FG,
        "axes.labelcolor": _FG,
        "axes.titlecolor": _FG,
        "text.color": _FG,
        "xtick.color": _FG,
        "ytick.color": _FG,
        "xtick.labelcolor": _FG,
        "ytick.labelcolor": _FG,
        "grid.color": _GRID,
        "grid.alpha": 0.30,
        "grid.linewidth": 0.8,
        "axes.grid": True,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "legend.frameon": False,
        "legend.labelcolor": _FG,
        "lines.linewidth": 2.0,
        "lines.markersize": 6,
        "axes.prop_cycle": mpl.cycler(color=_SERIES),
        "figure.figsize": (6.4, 3.8),
        "figure.dpi": 110,
    })


def _adaptify(svg: str) -> str:
    """Заменить цвета-маркеры на CSS-значения."""
    for i, c in enumerate(_SERIES, start=1):
        svg = svg.replace(c, f"var(--s{i})").replace(c.upper(), f"var(--s{i})")
    for c in (_GRID, _GRID.upper(), _FG, _FG.upper()):
        svg = svg.replace(c, "currentColor")
    # общий шрифт вместо зашитого matplotlib
    svg = re.sub(r"font-family:\s*[^;\"']+", f"font-family: {FONT_STACK}", svg)
    # адаптивная ширина: убрать жёсткие width/height у корневого <svg>, оставить viewBox
    svg = re.sub(r'(<svg[^>]*?)\s+width="[\d.]+pt"\s+height="[\d.]+pt"', r"\1", svg, count=1)
    return svg


def _component_name(stem: str) -> str:
    parts = [p for p in re.split(r"[^0-9A-Za-z]+", Path(stem).stem) if p]
    return "Fig" + "".join(p[:1].upper() + p[1:] for p in parts)


def save_adaptive(fig, stem: str, *, vue_dir: str | None = "components") -> Path:
    """Сохранить фигуру как адаптивный SVG и Vue-компонент для Slidev.

    stem — путь без расширения, например 'pics/cp'.
    """
    svg_path = Path(f"{stem}.svg")
    svg_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(svg_path, format="svg", bbox_inches="tight")
    svg = _adaptify(svg_path.read_text(encoding="utf-8"))
    svg_path.write_text(svg, encoding="utf-8")

    if vue_dir:
        name = _component_name(stem)
        body = svg[svg.index("<svg"):]
        out = Path(vue_dir) / f"{name}.vue"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            f"<!-- Сгенерировано figtheme.save_adaptive('{stem}') — не редактировать вручную -->\n"
            f"<template>\n{body}\n</template>\n", encoding="utf-8")
    return svg_path


def save_pair(fig, stem: str) -> tuple[Path, Path]:
    """Запасной вариант: два файла stem.svg и stem-dark.svg для <LightOrDark>.

    Нужен, если картинку хочется вставлять обычным `![](...)`, а не компонентом.
    """
    out: list[Path] = []
    for suffix, fg, series in ((".svg", "#1a1a19", PALETTE_LIGHT),
                               ("-dark.svg", "#e8eaed", PALETTE_DARK)):
        p = Path(f"{stem}{suffix}")
        p.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(p, format="svg", bbox_inches="tight")
        s = p.read_text(encoding="utf-8")
        for i, c in enumerate(_SERIES):
            repl = series[i % len(series)]
            s = s.replace(c, repl).replace(c.upper(), repl)
        for c in (_GRID, _GRID.upper(), _FG, _FG.upper()):
            s = s.replace(c, fg)
        s = re.sub(r"font-family:\s*[^;\"']+", f"font-family: {FONT_STACK}", s)
        p.write_text(s, encoding="utf-8")
        out.append(p)
    return out[0], out[1]
