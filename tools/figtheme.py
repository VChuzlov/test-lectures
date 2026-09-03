"""
figtheme.py — графики matplotlib и seaborn, подстраивающиеся под светлую и тёмную тему.

ИДЕЯ
----
Библиотека рисует график служебными цветами-маркерами, а после сохранения SVG
эти цвета заменяются на CSS-значения:

    обвязка графика (оси, текст, рамки, сетка) -> currentColor
    линии/столбцы/точки данных (серия 1..8)    -> var(--s1) ... var(--s8)

Один файл графика корректен и на светлом, и на тёмном фоне и переключается
мгновенно вместе с темой слайдов — без второй копии картинки.

ПОЧЕМУ ПРОСТОЙ ЗАМЕНЫ ЦВЕТА НЕДОСТАТОЧНО (важно для seaborn)
------------------------------------------------------------
seaborn не рисует теми цветами, которые ему дали. У barplot, boxplot,
violinplot и т. п. параметр `saturation` по умолчанию равен 0.75, то есть
заливка **обесцвечивается** перед отрисовкой. В SVG попадает уже другой цвет,
и точное совпадение строк его не находит.

Решение из двух частей:

1. Цвета-маркеры подобраны так, что у всех **светлота ровно 0.5**, а тона
   различны. Обесцвечивание меняет только насыщенность, а тон и светлоту
   сохраняет — значит, цвет всегда можно узнать обратно по паре (тон, светлота).
2. После точной замены идёт «восстановительный» проход: каждый оставшийся цвет
   переводится в HLS, и если пара (тон, светлота) совпала с маркером —
   он заменяется на нужную CSS-переменную.

Побочная выгода: маркеры теперь яркие и средней светлоты. Если замена почему-то
не сработает, на слайде будет видно кислотный цвет, а не чёрный прямоугольник,
который одинаково незаметен на обеих темах.

ИСПОЛЬЗОВАНИЕ
-------------
    import matplotlib.pyplot as plt, seaborn as sns
    from figtheme import use_adaptive, save_adaptive

    use_adaptive()                      # настраивает и matplotlib, и seaborn
    fig, ax = plt.subplots()
    sns.barplot(x=comp, y=frac, ax=ax)
    save_adaptive(fig, 'pics/bars')     # -> pics/bars.svg и components/FigBars.vue

В слайде:

    <FigBars class="w-[560px] mx-auto" />
"""
from __future__ import annotations

import colorsys
import re
import sys
from pathlib import Path

import matplotlib as mpl

# ─────────────────────────────────────────────────────────────────────────────
# Цвета-маркеры
#
# Все имеют светлоту 0.5 и полную насыщенность, тона выбраны в промежутках
# между «именными» цветами (red, yellow, lime, cyan, blue, magenta и т. д.),
# чтобы случайно не перехватить цвет, заданный вручную.
# ─────────────────────────────────────────────────────────────────────────────
_SENTINEL_L = 0.5
_SENTINEL_S = 1.0

_SERIES_HUES = [0.042, 0.125, 0.208, 0.292, 0.375, 0.458, 0.542, 0.625]
_FG_HUE = 0.708      # оси, текст, рамки, штрихи -> currentColor
_GRID_HUE = 0.792    # сетка                     -> currentColor


def _hue_to_hex(h: float) -> str:
    r, g, b = colorsys.hls_to_rgb(h, _SENTINEL_L, _SENTINEL_S)
    return "#%02x%02x%02x" % (round(r * 255), round(g * 255), round(b * 255))


def _hex_to_hls(hex_color: str) -> tuple[float, float, float]:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return colorsys.rgb_to_hls(r, g, b)


_SERIES = [_hue_to_hex(h) for h in _SERIES_HUES]
_FG = _hue_to_hex(_FG_HUE)
_GRID = _hue_to_hex(_GRID_HUE)

#: (тон, светлота) -> на что заменять
_SENTINEL_MAP: dict[str, str] = {}
for _i, _hex in enumerate(_SERIES, start=1):
    _SENTINEL_MAP[_hex] = f"var(--s{_i})"
_SENTINEL_MAP[_FG] = "currentColor"
_SENTINEL_MAP[_GRID] = "currentColor"

#: допуски восстановительного прохода.
#: обесцвечивание сохраняет тон и светлоту точно; расхождение даёт только
#: округление до 8 бит на канал — оно на порядок меньше этих значений
_TOL_H = 0.010
_TOL_L = 0.020

# ─────────────────────────────────────────────────────────────────────────────
# Палитра «для человека» — используется только в запасном режиме save_pair().
# Проверена на различимость при протанопии / дейтеранопии / тританопии
# отдельно на светлой (#fcfcfb) и тёмной (#1a1a19) подложке.
# ─────────────────────────────────────────────────────────────────────────────
PALETTE_LIGHT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]
PALETTE_DARK = ["#3987e5", "#d95926", "#199e70", "#c98500", "#d55181", "#008300"]

FONT_STACK = "Inter, 'Segoe UI', Roboto, Arial, sans-serif"


# ═════════════════════════════════════════════════════════════════════════════
# Настройка стиля
# ═════════════════════════════════════════════════════════════════════════════

def use_adaptive(*, seaborn_too: bool = True) -> None:
    """Включить стиль, пригодный для адаптивного экспорта.

    Настраивает matplotlib, а если seaborn установлен — и его тоже.

    Раскладку текста matplotlib считает своим шрифтом (DejaVu Sans),
    а в SVG подставляется шрифт страницы; для подписей осей расхождение
    метрик несущественно.
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
        "patch.edgecolor": _FG,
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

    if seaborn_too:
        _configure_seaborn()


def _configure_seaborn() -> None:
    """Заставить seaborn пользоваться нашими цветами-маркерами.

    seaborn не берёт палитру из axes.prop_cycle, когда рисует с `hue=`,
    поэтому её нужно задать явно.
    """
    try:
        import seaborn as sns
    except ImportError:
        return
    sns.set_palette(_SERIES)


def sns_kwargs(**extra) -> dict:
    """Аргументы seaborn, при которых цвета не искажаются.

    Не обязательно — восстановительный проход разбирает и обесцвеченные
    цвета. Но если хочется, чтобы в SVG сразу попадал точный маркер:

        sns.barplot(x=x, y=y, ax=ax, **sns_kwargs())
    """
    kw = {"saturation": 1.0}
    kw.update(extra)
    return kw


# ═════════════════════════════════════════════════════════════════════════════
# Преобразование SVG
# ═════════════════════════════════════════════════════════════════════════════

#: любой шестизначный цвет, не являющийся началом идентификатора
_HEX_RE = re.compile(r"#([0-9a-fA-F]{6})(?![0-9a-fA-F\w-])")


def _match_sentinel(hex_color: str) -> str | None:
    """Узнать цвет-маркер по тону и светлоте, даже если его обесцветили."""
    h, l, s = _hex_to_hls(hex_color)
    if s < 0.10:                       # обесцвечено до серого — тон недостоверен
        return None
    best, best_dh = None, _TOL_H
    for sentinel, repl in _SENTINEL_MAP.items():
        sh, sl, _ = _hex_to_hls(sentinel)
        if abs(l - sl) > _TOL_L:
            continue
        dh = min(abs(h - sh), 1.0 - abs(h - sh))   # тон замкнут в круг
        if dh <= best_dh:
            best, best_dh = repl, dh
    return best


def _is_surface_white(hex_color: str) -> bool:
    """Почти белый — это подложка, а не данные.

    seaborn красит белым окантовку маркеров scatterplot и линии медиан
    на тёмных заливках боксплота. Смысл этого цвета — «цвет фона»,
    поэтому он должен следовать за фоном страницы, а не оставаться белым
    (иначе на тёмной теме вокруг каждой точки светится ореол).
    """
    _, l, s = _hex_to_hls(hex_color)
    return l > 0.95 and s < 0.12


def _is_structural_gray(hex_color: str) -> bool:
    """Нейтральный тёмный серый — служебная графика seaborn.

    Так seaborn рисует усы, планки погрешностей и рамки боксплотов
    (по умолчанию серый .26 = #424242). На тёмном фоне такой цвет не виден,
    поэтому он тоже должен следовать за цветом текста.
    """
    h, l, s = _hex_to_hls(hex_color)
    return s < 0.12 and l < 0.60


def _adaptify(svg: str, *, verbose: bool = True,
              neutralize_grays: bool = True,
              neutralize_whites: bool = True) -> str:
    """Заменить цвета-маркеры на CSS-значения и подставить шрифт страницы.

    neutralize_grays  — нейтральный тёмный серый считать служебной графикой
                        seaborn и переводить в currentColor;
    neutralize_whites — почти белый считать подложкой и переводить в var(--surface).

    Оба правила нужно **выключать для heatmap и любых рисунков с непрерывной
    цветовой шкалой**: там цвет несёт данные, а подписи внутри ячеек seaborn
    красит чёрным или белым в зависимости от яркости ячейки — их нельзя
    привязывать к теме страницы, иначе на одной из тем они исчезнут.
    """
    stats = {"exact": 0, "recovered": 0, "gray": 0, "surface": 0}
    leftovers: dict[str, int] = {}

    def repl(m: re.Match) -> str:
        raw = m.group(0)
        low = "#" + m.group(1).lower()

        # 1. точное совпадение — обычный случай для matplotlib
        if low in _SENTINEL_MAP:
            stats["exact"] += 1
            return _SENTINEL_MAP[low]

        # 2. восстановление по тону и светлоте — случай seaborn с saturation<1
        found = _match_sentinel(low)
        if found:
            stats["recovered"] += 1
            return found

        # 3. служебный серый seaborn
        if neutralize_grays and _is_structural_gray(low):
            stats["gray"] += 1
            return "currentColor"

        # 4. почти белый — это подложка
        if neutralize_whites and _is_surface_white(low):
            stats["surface"] += 1
            return "var(--surface, #fcfcfb)"

        leftovers[low] = leftovers.get(low, 0) + 1
        return raw

    svg = _HEX_RE.sub(repl, svg)

    if verbose:
        parts = [f"{stats['exact']} точно"]
        if stats["recovered"]:
            parts.append(f"{stats['recovered']} восстановлено по тону")
        if stats["gray"]:
            parts.append(f"{stats['gray']} служебный серый")
        if stats["surface"]:
            parts.append(f"{stats['surface']} подложка")
        print(f"    цвета: {', '.join(parts)}")
        if leftovers:
            shown = sorted(leftovers.items(), key=lambda kv: -kv[1])[:6]
            tail = "" if len(leftovers) <= 6 else f" и ещё {len(leftovers) - 6}"
            print("    остались фиксированные цвета (не переключатся с темой): "
                  + ", ".join(f"{c}×{n}" for c, n in shown) + tail, file=sys.stderr)

    svg = re.sub(r"font-family:\s*[^;\"']+", f"font-family: {FONT_STACK}", svg)
    # адаптивная ширина: убрать жёсткие width/height, оставить viewBox
    svg = re.sub(r'(<svg[^>]*?)\s+width="[\d.]+pt"\s+height="[\d.]+pt"', r"\1", svg, count=1)
    return svg


def _clean_for_vue(svg: str, uid: str) -> str:
    """Убрать из SVG всё, на чём спотыкается компилятор шаблонов Vue."""
    # <metadata> с тегами rdf:/dc:/cc: — Vue принимает их за компоненты
    svg = re.sub(r"<metadata>.*?</metadata>", "", svg, flags=re.S)

    # <style> внутри <defs> -> те же правила атрибутами на корневом <svg>
    svg = re.sub(r"<style[^>]*>.*?</style>", "", svg, flags=re.S)
    svg = re.sub(r"<defs>\s*</defs>", "", svg)
    svg = svg.replace("<svg ", '<svg stroke-linejoin="round" stroke-linecap="butt" ', 1)

    # xlink -> href, убрать неиспользуемые namespace-объявления
    svg = svg.replace("xlink:href=", "href=")
    svg = re.sub(r'\s+xmlns:(xlink|dc|cc|rdf)="[^"]*"', "", svg)

    # уникализировать id и все ссылки на них
    ids = sorted(set(re.findall(r'id="([^"]+)"', svg)), key=len, reverse=True)
    for old in ids:
        new = f"{uid}-{old}"
        svg = svg.replace(f'id="{old}"', f'id="{new}"')
        svg = svg.replace(f'href="#{old}"', f'href="#{new}"')
        svg = svg.replace(f"url(#{old})", f"url(#{new})")

    return re.sub(r"\n\s*\n+", "\n", svg).strip()


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
    """Проверить готовый .vue на конструкции, ломающие сборку Slidev."""
    text = Path(path).read_text(encoding="utf-8")
    return [f"{needle}  — {why}" for needle, why in _FORBIDDEN.items() if needle in text]


def _component_name(stem: str) -> str:
    parts = [p for p in re.split(r"[^0-9A-Za-z]+", Path(stem).stem) if p]
    return "Fig" + "".join(p[:1].upper() + p[1:] for p in parts)


# ═════════════════════════════════════════════════════════════════════════════
# Сохранение
# ═════════════════════════════════════════════════════════════════════════════

def save_adaptive(fig, stem: str, *, vue_dir: str | None = "components",
                  verbose: bool = True,
                  neutralize_grays: bool = True,
                  neutralize_whites: bool = True) -> Path:
    """Сохранить фигуру как адаптивный SVG и Vue-компонент для Slidev.

    stem — путь без расширения, например 'pics/bars'.

    Для heatmap и других рисунков с непрерывной цветовой шкалой вызывайте
    с neutralize_grays=False, neutralize_whites=False — иначе подписи
    внутри ячеек привяжутся к теме страницы и на одной из тем пропадут.
    """
    svg_path = Path(f"{stem}.svg")
    svg_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(svg_path, format="svg", bbox_inches="tight")

    svg = _adaptify(svg_path.read_text(encoding="utf-8"), verbose=verbose,
                    neutralize_grays=neutralize_grays,
                    neutralize_whites=neutralize_whites)
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
            print(f"    ВНИМАНИЕ: в {out} осталось то, что сломает сборку:", file=sys.stderr)
            for p in problems:
                print(f"      - {p}", file=sys.stderr)
        elif verbose:
            print(f"    {out}  — чисто")
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

        def repl(m: re.Match, _fg=fg, _series=series, suffix=suffix) -> str:
            low = "#" + m.group(1).lower()
            if low in (_FG, _GRID):
                return _fg
            if low in _SERIES:
                return _series[_SERIES.index(low) % len(_series)]
            found = _match_sentinel(low)
            if found == "currentColor":
                return _fg
            if found:
                idx = int(found[len("var(--s"):-1]) - 1
                return _series[idx % len(_series)]
            if _is_structural_gray(low):
                return _fg
            if _is_surface_white(low):
                return "#ffffff" if suffix == ".svg" else "#1a1a19"
            return m.group(0)

        s = _HEX_RE.sub(repl, s)
        s = re.sub(r"font-family:\s*[^;\"']+", f"font-family: {FONT_STACK}", s)
        p.write_text(s, encoding="utf-8")
        out.append(p)
    return out[0], out[1]


if __name__ == "__main__":
    # python tools/figtheme.py lectures/*/components/*.vue — проверить компоненты
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
