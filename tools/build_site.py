#!/usr/bin/env python3
"""
build_site.py — собрать все лекции в один статический сайт с оглавлением.

Что делает:
  1. Находит все папки lectures/*/slides.md
  2. Для каждой запускает `npx slidev build` с правильным --base
  3. Кладёт результат в dist/<имя-папки>/
  4. Генерирует dist/index.html — страницу-оглавление со светлой/тёмной темой

Запуск:
    python tools/build_site.py                     # для GitHub Pages в корне домена
    python tools/build_site.py --base /kurs-2026/  # если репозиторий = подпапка
    python tools/build_site.py --only lec-03       # пересобрать одну лекцию

Метаданные лекции берутся из headmatter slides.md (title, info, а также
необязательные поля `lecture:` и `topics:`).
"""
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LECTURES = ROOT / "lectures"
DIST = ROOT / "dist"


def read_headmatter(slides: Path) -> dict:
    """Минимальный разбор YAML-шапки без внешних зависимостей."""
    text = slides.read_text(encoding="utf-8")
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    meta: dict[str, str] = {}
    if not m:
        return meta
    for line in m.group(1).splitlines():
        if line.startswith((" ", "\t", "#")) or ":" not in line:
            continue
        k, _, v = line.partition(":")
        v = v.strip().strip("'\"")
        if v and v != "|":
            meta[k.strip()] = v
    return meta


def build_one(folder: Path, base: str) -> None:
    out = DIST / folder.name
    print(f"  → сборка {folder.name}")
    subprocess.run(
        ["npx", "--yes", "slidev", "build",
         "--base", f"{base}{folder.name}/",
         "--out", str(out)],
        cwd=folder, check=True,
    )


def render_index(cards: list[dict], base: str) -> str:
    items = "\n".join(
        f"""      <a class="card" href="{html.escape(base + c['slug'] + '/')}">
        <div class="num">{html.escape(c['num'])}</div>
        <div class="body">
          <h2>{html.escape(c['title'])}</h2>
          <p>{html.escape(c['topics'])}</p>
        </div>
        <div class="go">→</div>
      </a>"""
        for c in cards
    )
    return f"""<!doctype html>
<html lang="ru" data-theme="auto">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Основы программирования — лекции</title>
<style>
  :root {{
    color-scheme: light;
    --surface:#fcfcfb; --surface-2:#ffffff; --ink:#1a1a19; --ink-2:#52514e;
    --line:#e2e2de; --brand:#0f7a3d; --brand-2:#12a05e; --shadow:0 1px 2px rgba(0,0,0,.06),0 8px 24px rgba(0,0,0,.05);
  }}
  html.dark {{
    color-scheme: dark;
    --surface:#141413; --surface-2:#1f1f1d; --ink:#e8eaed; --ink-2:#a9a89f;
    --line:#33332f; --brand:#2bb671; --brand-2:#4ed48a; --shadow:0 1px 2px rgba(0,0,0,.4);
  }}
  * {{ box-sizing:border-box; }}
  body {{
    margin:0; background:var(--surface); color:var(--ink);
    font:16px/1.55 Inter,'Segoe UI',Roboto,Arial,sans-serif;
    -webkit-font-smoothing:antialiased;
  }}
  .wrap {{ max-width:860px; margin:0 auto; padding:48px 20px 80px; }}
  header {{ display:flex; align-items:flex-start; justify-content:space-between; gap:16px; margin-bottom:36px; }}
  h1 {{
    font-size:2rem; line-height:1.2; margin:0 0 6px; font-weight:700;
    background-image:linear-gradient(45deg,var(--brand-2) 10%,var(--brand) 70%);
    background-clip:text; -webkit-background-clip:text; color:transparent;
  }}
  .sub {{ color:var(--ink-2); margin:0; }}
  button.theme {{
    background:var(--surface-2); color:var(--ink); border:1px solid var(--line);
    border-radius:999px; padding:8px 14px; cursor:pointer; font:inherit; font-size:.9rem;
    white-space:nowrap;
  }}
  button.theme:hover {{ border-color:var(--brand); color:var(--brand); }}
  .grid {{ display:flex; flex-direction:column; gap:10px; }}
  .card {{
    display:flex; align-items:center; gap:16px; text-decoration:none; color:inherit;
    background:var(--surface-2); border:1px solid var(--line); border-radius:12px;
    padding:14px 18px; box-shadow:var(--shadow); transition:border-color .15s, transform .15s;
  }}
  .card:hover {{ border-color:var(--brand); transform:translateY(-1px); }}
  .num {{
    flex:0 0 auto; width:40px; height:40px; border-radius:10px;
    background:var(--brand); color:#fff; display:grid; place-items:center;
    font-weight:700; font-size:.95rem;
  }}
  html.dark .num {{ color:#0b2318; }}   /* тёмный текст на светлом зелёном — читаемее белого */
  .body {{ flex:1 1 auto; min-width:0; }}
  .card h2 {{ font-size:1rem; margin:0 0 2px; font-weight:600; }}
  .card p {{ margin:0; color:var(--ink-2); font-size:.87rem; }}
  .go {{ color:var(--ink-2); font-size:1.2rem; }}
  footer {{ margin-top:40px; color:var(--ink-2); font-size:.85rem; }}
  @media (max-width:520px) {{ .wrap {{ padding:28px 14px 60px; }} h1 {{ font-size:1.5rem; }} }}
</style>
</head>
<body>
  <div class="wrap">
    <header>
      <div>
        <h1>Основы программирования</h1>
        <p class="sub">Химическая технология · 1 курс · Python</p>
      </div>
      <button class="theme" id="t">Тема: авто</button>
    </header>
    <main class="grid">
{items}
    </main>
    <footer>Слайды открываются в браузере телефона и ноутбука. Клавиша <b>d</b> внутри лекции — смена темы, <b>o</b> — обзор всех слайдов, <b>f</b> — полный экран.</footer>
  </div>
<script>
  // Тема: авто → светлая → тёмная. Выбор запоминается в этой вкладке.
  const modes = ['auto','light','dark'], labels = {{auto:'авто', light:'светлая', dark:'тёмная'}};
  let i = 0;
  const mq = window.matchMedia('(prefers-color-scheme: dark)');
  const btn = document.getElementById('t');
  function apply() {{
    const m = modes[i];
    const dark = m === 'dark' || (m === 'auto' && mq.matches);
    document.documentElement.classList.toggle('dark', dark);
    btn.textContent = 'Тема: ' + labels[m];
  }}
  btn.onclick = () => {{ i = (i + 1) % modes.length; apply(); }};
  mq.addEventListener('change', apply);
  apply();
</script>
</body>
</html>
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="/", help="базовый путь сайта, например /kurs-2026/")
    ap.add_argument("--only", help="собрать только одну лекцию (имя папки)")
    ap.add_argument("--index-only", action="store_true", help="пересобрать только оглавление")
    args = ap.parse_args()

    base = args.base if args.base.endswith("/") else args.base + "/"

    folders = sorted(p.parent for p in LECTURES.glob("*/slides.md"))
    if not folders:
        print(f"Не найдено ни одной лекции в {LECTURES}", file=sys.stderr)
        return 1
    if args.only:
        folders = [f for f in folders if f.name == args.only]

    DIST.mkdir(exist_ok=True)

    cards = []
    for f in folders:
        meta = read_headmatter(f / "slides.md")
        if not args.index_only:
            build_one(f, base)
        cards.append({
            "slug": f.name,
            "num": meta.get("lecture", re.sub(r"\D", "", f.name) or "•"),
            "title": meta.get("title", f.name),
            "topics": meta.get("topics", ""),
        })

    (DIST / "index.html").write_text(render_index(cards, base), encoding="utf-8")
    # .nojekyll нужен, чтобы GitHub Pages не съел папки, начинающиеся с _
    (DIST / ".nojekyll").write_text("", encoding="utf-8")
    print(f"\nГотово: {DIST}/index.html ({len(cards)} лекций)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
