"""
figtheme.py — графики matplotlib, которые сами подстраиваются под светлую и тёмную тему.

ИДЕЯ
----
matplotlib рисует график служебными цветами-маркерами, а после сохранения SVG
эти цвета заменяются на CSS-значения:

    обвязка графика (оси, текст, рамки, сетка) -> currentColor
    линии/точки данных (серия 1..8)            -> var(--s1) ... var(--s8)

Один файл графика корректен и на светлом, и на тёмном фоне и переключается
мгновенно вместе с темой слайдов — без второй копии картинки.

ВАЖНО: currentColor и var(--s1) работают только для ИНЛАЙНОВОГО SVG в DOM.
Через <img src="fig.svg"> они не работают. Поэтому save_adaptive() дополнительно
кладёт готовый Vue-компонент в components/, а Slidev подхватывает его сам.

ПОЧЕМУ SVG ПРИХОДИТСЯ ЧИСТИТЬ
-----------------------------
matplotlib пишет в SVG служебный XML, безвредный в обычном файле, но ломающий
сборку внутри <template> Vue:

  * <metadata> с тегами <rdf:RDF>, <dc:*>, <cc:*> — Vue считает их компонентами
    и падает с "Failed to resolve component: rdf:RDF";
  * <style> внутри <defs> — Vue не обрабатывает теги с побочным эффектом в шаблоне;
  * xlink:href — устаревшая форма, в SVG2 достаточно href;
  * id вида figure_1 / patch_1 одинаковы у всех фигур: два графика на одном
    слайде — и ссылки url(#...) начинают указывать не туда.

Всё это снимает _clean_for_vue(). Функция check_vue() проверяет результат
и выдаёт понятное сообщение, если что-то просочилось.

ИСПОЛЬЗОВАНИЕ
-------------
    import numpy as np, matplotlib.pyplot as plt
    from figtheme import use_adaptive, save_adaptive

    use_adaptive()
    fig, ax = plt.subplots()
    ax.plot(T, cp, label='1-гексен')
    ax.set_xlabel('T, K'); ax.legend()
    save_adaptive(fig, 'pics/cp')      # -> pics/cp.svg и components/FigCp.vue

В слайде:

    <FigCp class="w-[560px] mx-auto" />
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import matplotlib as mpl

# ── служебные цвета-маркеры (реальными данными их не используем) ──────────────
_FG = "#010203"      # оси, текст, рамки, штрихи  -> currentColor
_GRID = "#040506"    # сетка                      -> currentColor + opacity
_SERIES = [f"#1000{i:02d}" for i in range(1, 9)]   # #100001 ... #100008 -> var(--sN)

# ── палитра «для человека»: используется в запасном режиме save_pair() ────────
# Проверена на различимость при протанопии / дейтеранопии / тританопии
# отдельно на светлой (#fcfcfb) и тёмной (#1a1a19) подложке.
PALETTE_LIGHT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]
PALETTE_DARK = ["#3987e5", "#d95926", "#199e70", "#c98500", "#d55181", "#008300"]

FONT_STACK = "Inter, 'Segoe UI', Roboto, Arial, sans-serif"


def use_adaptive() -> None:
    """Включить стиль, пригодный для адаптивного экспорта."""
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
    """Заменить цвета-маркеры на CSS-значения и подставить шрифт страницы."""
    for i, c in enumerate(_SERIES, start=1):
        svg = svg.replace(c, f"var(--s{i})").replace(c.upper(), f"var(--s{i})")
    for c in (_GRID, _GRID.upper(), _FG, _FG.upper()):
        svg = svg.replace(c, "currentColor")
    svg = re.sub(r"font-family:\s*[^;\"']+", f"font-family: {FONT_STACK}", svg)
    # адаптивная ширина: убрать жёсткие width/height, оставить viewBox
    svg = re.sub(r'(<svg[^>]*?)\s+width="[\d.]+pt"\s+height="[\d.]+pt"', r"\1", svg, count=1)
    return svg


def _clean_for_vue(svg: str, uid: str) -> str:
    """Убрать из SVG всё, на чём спотыкается компилятор шаблонов Vue."""
    # 1. служебные метаданные с namespace-тегами
    svg = re.sub(r"<metadata>.*?</metadata>", "", svg, flags=re.S)

    # 2. <style> внутри <defs> -> те же правила атрибутами на корневом <svg>
    svg = re.sub(r"<style[^>]*>.*?</style>", "", svg, flags=re.S)
    svg = re.sub(r"<defs>\s*</defs>", "", svg)
    svg = svg.replace("<svg ", '<svg stroke-linejoin="round" stroke-linecap="butt" ', 1)

    # 3. xlink -> href, убрать неиспользуемые namespace-объявления
    svg = svg.replace("xlink:href=", "href=")
    svg = re.sub(r'\s+xmlns:(xlink|dc|cc|rdf)="[^"]*"', "", svg)

    # 4. уникализировать id и все ссылки на них
    ids = sorted(set(re.findall(r'id="([^"]+)"', svg)), key=len, reverse=True)
    for old in ids:
        new = f"{uid}-{old}"
        svg = svg.replace(f'id="{old}"', f'id="{new}"')
        svg = svg.replace(f'href="#{old}"', f'href="#{new}"')
        svg = svg.replace(f"url(#{old})", f"url(#{new})")

    # 5. схлопнуть пустые строки, оставшиеся после удалений
    svg = re.sub(r"\n\s*\n+", "\n", svg)
    return svg.strip()


#: конструкции, из-за которых Slidev падает при сборке компонента
_FORBIDDEN = {
    "<metadata": "служебные метаданные matplotlib с тегами rdf:/dc:/cc:",
    "<style": "тег <style> внутри шаблона Vue",
    "<script": "тег <script> внутри шаблона Vue",
    "rdf:": "namespace-тег, Vue примет его за компонент",
    "dc:": "namespace-тег, Vue примет его за компонент",
    "cc:": "namespace-тег, Vue примет его за компонент",
    "xlink:": "устаревший атрибут, в SVG2 достаточно href",
}


def check_vue(path: str | Path) -> list[str]:
    """Проверить готовый .vue на конструкции, ломающие сборку Slidev.

    Возвращает список проблем (пустой список = всё в порядке).
    """
    text = Path(path).read_text(encoding="utf-8")
    return [f"{needle}  — {why}" for needle, why in _FORBIDDEN.items() if needle in text]


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
    svg_path.write_text(svg, encoding="utf-8")   # чистый .svg — для <img> и печати

    if vue_dir:
        name = _component_name(stem)
        body = _clean_for_vue(svg[svg.index("<svg"):], uid=Path(stem).stem)
        out = Path(vue_dir) / f"{name}.vue"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            f"<!-- Сгенерировано figtheme.save_adaptive('{stem}') — не редактировать вручную -->\n"
            f"<template>\n{body}\n</template>\n", encoding="utf-8")

        problems = check_vue(out)
        if problems:
            print(f"  ВНИМАНИЕ: в {out} осталось то, что сломает сборку:", file=sys.stderr)
            for p in problems:
                print(f"    - {p}", file=sys.stderr)
        else:
            print(f"  {out}  — чисто")
    return svg_path


def save_pair(fig, stem: str) -> tuple[Path, Path]:
    """Запасной вариант: два файла stem.svg и stem-dark.svg для <LightOrDark>.

    Нужен, если картинку хочется вставлять обычным ![](...), а не компонентом.
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


if __name__ == "__main__":
    # python tools/figtheme.py lectures/*/components/*.vue — проверить готовые компоненты
    bad = False
    for arg in sys.argv[1:]:
        problems = check_vue(arg)
        if problems:
            bad = True
            print(f"{arg}:")
            for p in problems:
                print(f"  - {p}")
        else:
            print(f"{arg}: чисто")
    sys.exit(1 if bad else 0)
