#!/usr/bin/env python3
"""
slides2notes.py — сделать из слайдов Slidev страницы конспекта для VitePress.

Источник один: lectures/<папка>/slides.md. Конспект генерируется при каждой
сборке, поэтому руками его не правят — правят слайды.

Что делает с каждым slides.md:
  * режет файл на слайды (разделитель ---, шапка слайда layout:/image: и т.п.);
  * титульный и финальный слайды пропускает, шапку лекции превращает
    в заголовок страницы;
  * слайд-разделитель раздела (layout: image-*) -> заголовок ## ;
    обычный слайд -> ### ; слайды-продолжения с тем же заголовком
    сливаются под одним заголовком;
  * у каждого заголовка якорь #slide-N и ссылка «слайд N» на презентацию;
  * <v-click>…</v-click> -> раскрывающийся блок «Ответ»: в аудитории
    ответ открывается по клику, дома студент сначала думает сам;
  * заметки докладчика (комментарий в конце слайда) в конспект НЕ попадают:
    это подсказки для вас («сначала спросить зал»), а не для студентов;
  * текст, который нужен только в конспекте, пишите на слайде в
        <div class="konspekt">…</div>
    — на слайдах он скрыт (правило в shared/style.css), в конспекте виден;
  * картинки ./pics/… и компоненты <FigXxx/> копирует рядом со страницей,
    style.css лекции — тоже (правила .slidev-layout -> .vp-doc).

Запуск (из корня репозитория):
    python tools/slides2notes.py                 # все лекции
    python tools/slides2notes.py --only lec-04   # одна лекция
    python tools/slides2notes.py --slides-base /test-lectures/
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LECTURES = ROOT / "lectures"
SITE = ROOT / "site"
OUT = SITE / "konspekt"          # страницы конспекта: /konspekt/lec-04/

SEP = re.compile(r"^---\s*$")
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
YAML_KEY = re.compile(r"^[A-Za-z_][\w-]*\s*:")


# ─────────────────────────── разбор slides.md ──────────────────────────────

def parse_yaml_flat(lines: list[str]) -> dict[str, str]:
    """Плоский YAML: только ключ: значение верхнего уровня."""
    meta: dict[str, str] = {}
    for line in lines:
        if not YAML_KEY.match(line):
            continue
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip().strip("'\"")
    return meta


def looks_like_frontmatter(block: list[str]) -> bool:
    body = [l for l in block if l.strip()]
    if not body or not YAML_KEY.match(body[0]):
        return False
    return all(YAML_KEY.match(l) or l.startswith((" ", "\t", "#")) for l in body)


def fence_state(line: str, fence: str | None) -> str | None:
    """Открыт ли блок кода после этой строки (``` или ~~~ любой длины)."""
    m = FENCE.match(line)
    if not m:
        return fence
    mark = m.group(1)
    if fence is None:
        return mark
    if mark[0] == fence[0] and len(mark) >= len(fence) and line.strip() == mark:
        return None
    return fence


def split_slides(text: str) -> tuple[dict, list[dict]]:
    lines = text.replace("\r\n", "\n").split("\n")
    head: dict[str, str] = {}
    i = 0
    if lines and SEP.match(lines[0]):
        j = next(k for k in range(1, len(lines)) if SEP.match(lines[k]))
        head = parse_yaml_flat(lines[1:j])
        i = j + 1

    slides: list[dict] = []
    cur: list[str] = []
    fm: dict[str, str] = {}
    fence: str | None = None
    while i < len(lines):
        ln = lines[i]
        fence = fence_state(ln, fence)
        if fence is None and SEP.match(ln):
            slides.append({"fm": fm, "lines": cur})
            cur, fm = [], {}
            k, block = i + 1, []
            while k < len(lines) and not SEP.match(lines[k]):
                block.append(lines[k])
                k += 1
            if k < len(lines) and looks_like_frontmatter(block):
                fm = parse_yaml_flat(block)
                i = k + 1
                continue
            i += 1
            continue
        cur.append(ln)
        i += 1
    slides.append({"fm": fm, "lines": cur})
    for n, s in enumerate(slides, start=1):
        s["no"] = n            # номер слайда в презентации (титул = 1)
        s["text"] = "\n".join(s.pop("lines")).strip("\n")
    return head, slides


# ─────────────────────────── обработка слайда ──────────────────────────────

TRAILING_NOTE = re.compile(r"\n*<!--((?:(?!<!--).)*?)-->\s*$", re.S)
SLIDE_NO = re.compile(r'^\s*<div class=["\']slide-no["\']>.*?</div>\s*$', re.M)
MUSTACHE_NAV = re.compile(r"\{\{[^}]*\$(?:nav|slidev|clicks|page)[^}]*\}\}")
ONLY_BR = re.compile(r"^\s*(?:<br\s*/?>\s*)+$", re.M)
V_ATTR = re.compile(r"\s+v-(?:click|after|click-hide)(?:=\"[^\"]*\")?(?=[\s>/])")
IMG_SRC = re.compile(r"""(src\s*=\s*['"])\./(pics/[^'"]+)(['"])""")
MD_IMG = re.compile(r"(!\[[^\]]*\]\()\./(pics/[^)\s]+)")
FIG = re.compile(r"<(Fig[A-Z]\w*)\b")


def strip_code(text: str) -> str:
    """Текст без содержимого блоков кода — чтобы искать заголовки и теги."""
    return re.sub(r"(^|\n)(`{3,}|~{3,}).*?\n\2[ \t]*(?=\n|$)", r"\1", text, flags=re.S)


def title_of(text: str) -> str | None:
    m = re.search(r"^#\s+(.+?)\s*$", strip_code(text), re.M)
    return m.group(1) if m else None


def drop_first_h1(text: str) -> str:
    out, fence, done = [], None, False
    for ln in text.split("\n"):
        was = fence
        fence = fence_state(ln, fence)
        if was is not None or fence is not None:
            out.append(ln)
            continue
        if not done and re.match(r"^#\s+", ln):
            done = True
            continue
        out.append(ln)
    return "\n".join(out)


def demote_headings(text: str, to: int) -> str:
    """Подзаголовки внутри слайда (##, ###, ####) -> один уровень `to`."""
    out, fence = [], None
    for ln in text.split("\n"):
        was = fence
        fence = fence_state(ln, fence)
        if was is None and fence is None:
            h = re.match(r"^(#{2,6})(\s+.*)$", ln)
            if h:
                ln = "#" * to + h.group(2)
        out.append(ln)
    return "\n".join(out)


def v_click_to_details(text: str) -> str:
    text = re.sub(r"<v-clicks?[^>]*>", '\n<details class="details custom-block answer">'
                  '<summary>Ответ</summary>\n', text)
    text = re.sub(r"</v-clicks?>", "\n</details>\n", text)
    return V_ATTR.sub("", text)


HTML_TAG = re.compile(r"<[A-Za-z][^<>]*>")


def outside_code(text: str, fn) -> str:
    """Применить fn только к тексту вне блоков кода."""
    out, chunk, fence = [], [], None
    for ln in text.split("\n"):
        was = fence
        fence = fence_state(ln, fence)
        if was is None and fence is None:
            chunk.append(ln)
            continue
        if chunk:
            out.append(fn("\n".join(chunk)))
            chunk = []
        out.append(ln)
    if chunk:
        out.append(fn("\n".join(chunk)))
    return "\n".join(out)


def fix_html(text: str) -> str:
    # <img src='a.svg', width=370>: запятая между атрибутами. Slidev её
    # прощает, а Vue в браузере падает на ней, и страница не открывается.
    text = HTML_TAG.sub(lambda m: re.sub(r"""(['"])\s*,(?=\s)""", r"\1", m.group(0)), text)
    # <center> устарел и Vue считает его компонентом -> обычный div
    text = text.replace("<center>", '<div class="center">').replace("</center>", "</div>")
    return text


def clean_slide(text: str) -> tuple[str, str | None]:
    note = None
    m = TRAILING_NOTE.search(text)
    if m:
        note = m.group(1).strip()
        text = text[: m.start()]
    text = SLIDE_NO.sub("", text)
    text = MUSTACHE_NAV.sub("", text)
    text = ONLY_BR.sub("", text)
    text = outside_code(text, fix_html)
    text = v_click_to_details(text)
    return text.strip("\n"), note


def is_section(slide: dict) -> bool:
    if not slide["fm"].get("layout", "").startswith(("image", "section")):
        return False
    rest = drop_first_h1(slide["text"])
    rest = TRAILING_NOTE.sub("", SLIDE_NO.sub("", rest))
    return not rest.strip()


def is_cover_or_end(slide: dict) -> bool:
    t = slide["text"]
    return "cover-bg" in t or "Благодарю за внимание" in t or "Спасибо за внимание" in t


# ─────────────────────────── сборка страницы ───────────────────────────────

def slide_ref(nos: list[int], slide_prefix: str) -> str:
    label = f"{nos[0]}" if len(nos) == 1 else f"{nos[0]}–{nos[-1]}"
    return (f'<a class="slide-ref ignore-header" href="{slide_prefix}{nos[0]}" '
            f'target="_blank" rel="noopener" data-label="{label}" '
            f'title="Открыть на слайдах"></a>')


def convert(folder: Path, slides_base: str) -> dict:
    head, slides = split_slides((folder / "slides.md").read_text(encoding="utf-8"))
    num = head.get("lecture", folder.name.split("-")[-1]).lstrip("0") or "0"
    title = head.get("title", folder.name)
    topics = [t.strip() for t in head.get("topics", "").split(",") if t.strip()]
    slides_url = f"{slides_base}{folder.name}/"
    # routerMode: hash -> адрес слайда …/lec-04/#/17; работает и при
    # обновлении страницы на GitHub Pages. При history -> …/lec-04/17
    slide_prefix = slides_url + ("#/" if head.get("routerMode") == "hash" else "")

    out_dir = OUT / folder.name
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    body: list[str] = []
    section: str | None = None
    prev_title: str | None = None
    last_ref_idx: int | None = None
    sec_idx: int | None = None
    ref_nos: list[int] = []
    notes_skipped = 0
    for s in slides:
        if is_cover_or_end(s):
            continue
        if s["fm"].get("hide") in ("true", "True") or s["fm"].get("disabled") in ("true", "True"):
            continue
        t = title_of(s["text"])
        if is_section(s):
            section = t
            body.append(f"\n## {t} {{#slide-{s['no']}}}\n")
            prev_title, last_ref_idx, sec_idx = t, None, len(body) - 1
            continue
        text, note = clean_slide(drop_first_h1(s["text"]))
        notes_skipped += bool(note)
        level = "###" if section else "##"
        text = demote_headings(text, to=len(level) + 1)
        if t and t != prev_title:
            ref_nos = [s["no"]]
            body.append(f"\n{level} {t} {slide_ref(ref_nos, slide_prefix)} {{#slide-{s['no']}}}\n")
            last_ref_idx = len(body) - 1
        elif last_ref_idx is not None:          # продолжение: «слайды 22–24»
            ref_nos.append(s["no"])
            body[last_ref_idx] = re.sub(r'<a class="slide-ref.*?</a>', slide_ref(ref_nos, slide_prefix),
                                        body[last_ref_idx])
        elif sec_idx is not None:               # сразу после разделителя с тем же заголовком
            ref_nos = [s["no"]]
            body[sec_idx] = body[sec_idx].replace(" {#", f" {slide_ref(ref_nos, slide_prefix)} {{#", 1)
            last_ref_idx = sec_idx
        prev_title = t or prev_title
        if text.strip():
            body.append(text + "\n")

    md = "\n".join(body)

    # картинки ./pics/… -> копия рядом со страницей
    for rel in {m[1] for m in IMG_SRC.findall(md)} | {m[1] for m in MD_IMG.findall(md)}:
        src = folder / rel
        if src.exists():
            (out_dir / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, out_dir / rel)
        else:
            print(f"    ! нет файла {rel}")

    # компоненты <FigXxx/>: из папки лекции, иначе из общей components/
    imports = []
    for name in sorted(set(FIG.findall(md))):
        for cand in (folder / "components" / f"{name}.vue", ROOT / "components" / f"{name}.vue"):
            if cand.exists():
                (out_dir / "components").mkdir(exist_ok=True)
                shutil.copy2(cand, out_dir / "components" / cand.name)
                imports.append(f"import {name} from './components/{name}.vue'")
                break
        else:
            print(f"    ! нет компонента {name}")

    # style.css лекции: без @import и титульного фона, .slidev-layout -> .vp-doc
    css_import = ""
    if (folder / "style.css").exists():
        css = (folder / "style.css").read_text(encoding="utf-8")
        css = re.sub(r"@import[^;]+;", "", css)
        css = re.sub(r"(?:html\.dark\s+)?\.cover-bg\s*\{[^}]*\}", "", css)
        css = css.replace(".slidev-layout", ".vp-doc")
        (out_dir / "style.css").write_text(css, encoding="utf-8")
        css_import = "import './style.css'"

    script = "\n".join(filter(None, [css_import, *imports]))
    chips = "".join(f"<span>{t}</span>" for t in topics)
    updated = git_date(folder / "slides.md")
    updated_line = f"lastUpdated: {updated}\n" if updated else "lastUpdated: false\n"
    page = f"""---
title: {json.dumps(f"Лекция {num}. {title}", ensure_ascii=False)}
outline: [2, 3]
{updated_line}---

<script setup>
{script}
</script>

<div class="lec-eyebrow">Лекция {num}</div>

# {title}

<div class="lec-topics">{chips}</div>

<div class="lec-links">
<a class="lec-btn" href="{slides_url}" target="_blank" rel="noopener">Открыть слайды</a>
<span class="lec-hint">Вопросы из лекции спрятаны в блоки «Ответ»: сначала подумайте сами.</span>
</div>

{md}
"""
    (out_dir / "index.md").write_text(page, encoding="utf-8")
    shown = sum(1 for s in slides if not is_cover_or_end(s))
    print(f"  {folder.name}: {shown} слайдов -> {out_dir.relative_to(ROOT)}/index.md"
          f"  (заметок докладчика пропущено: {notes_skipped})")
    return {"folder": folder.name, "lecture": num, "title": title, "topics": topics,
            "slides": slides_url}


def git_date(path: Path) -> str | None:
    """Дата последнего коммита slides.md — её студент видит как «Обновлено»."""
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cI", "--", path.name],
                             cwd=path.parent, capture_output=True, text=True, timeout=10)
        return out.stdout.strip() or None
    except (OSError, subprocess.SubprocessError):
        return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="одна папка лекции, например lec-04")
    ap.add_argument("--slides-base", default="/",
                    help="адрес, под которым лежат собранные слайды: <slides-base><папка>/ "
                         "(на GitHub Pages это /<репозиторий>/)")
    args = ap.parse_args()

    folders = sorted(p.parent for p in LECTURES.glob("*/slides.md"))
    if args.only:
        folders = [f for f in folders if f.name == args.only]
    print("Конспекты:")
    index = [convert(f, args.slides_base) for f in folders]
    if not args.only:
        (SITE / ".vitepress" / "lectures.json").write_text(
            json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
