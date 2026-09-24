---
layout: home

hero:
  name: Основы программирования
  text: Лекции и конспекты
  tagline: Python для химиков-технологов · ОХИ ИШПР ТПУ · 2026/27
---

<script setup>
import { data as lectures } from './lectures.data.js'
import { withBase } from 'vitepress'
</script>

<div class="lec-grid">
  <div v-for="l in lectures" :key="l.folder" class="lec-card">
    <span class="lec-card-no">Лекция {{ l.lecture }}</span>
    <a class="lec-card-title" :href="withBase(`/konspekt/${l.folder}/`)">{{ l.title }}</a>
    <span class="lec-card-topics">{{ l.topics.join(' · ') }}</span>
    <span class="lec-card-links">
      <a class="primary" :href="withBase(`/konspekt/${l.folder}/`)">Конспект</a>
      <a :href="l.slides" target="_blank" rel="noopener">Слайды</a>
    </span>
  </div>
</div>

<p class="lec-keys">В слайдах: <kbd>d</kbd> — смена темы, <kbd>o</kbd> — обзор всех слайдов, <kbd>f</kbd> — полный экран.</p>

<style>
.lec-grid {
  max-width: 1152px;
  margin: 0 auto 24px;
  padding: 0 24px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 16px;
}
.lec-card {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 20px 22px;
  border-radius: 12px;
  border: 1px solid var(--line);
  background: var(--surface-2);
  transition: border-color .15s;
}
.lec-card:hover { border-color: var(--brand); }
.vp-doc .lec-card a { text-decoration: none; }
.lec-card-no { font-size: 0.75rem; font-weight: 600; letter-spacing: .1em; text-transform: uppercase; color: var(--brand); }
.vp-doc a.lec-card-title { font-size: 1.05rem; font-weight: 600; color: var(--ink); line-height: 1.35; }
.vp-doc a.lec-card-title:hover { color: var(--brand); }
.lec-card-topics { font-size: 0.82rem; color: var(--ink-muted); line-height: 1.45; flex: 1; }
.lec-card-links { display: flex; gap: 8px; margin-top: 8px; }
.vp-doc .lec-card-links a {
  font-size: 0.85rem; font-weight: 600; padding: 4px 12px; border-radius: 8px;
  border: 1px solid var(--line); color: var(--ink-2);
}
.vp-doc .lec-card-links a:hover { border-color: var(--brand); color: var(--brand); }
.vp-doc .lec-card-links a.primary { background: var(--brand); border-color: var(--brand); color: var(--surface); }
.vp-doc .lec-card-links a.primary:hover { background: var(--brand-2); color: var(--surface); }
.lec-keys { max-width: 1152px; margin: 0 auto 64px; padding: 0 24px; font-size: 0.85rem; color: var(--ink-muted); }
.lec-keys kbd { font-family: var(--code-font); border: 1px solid var(--line); border-bottom-width: 2px; border-radius: 5px; padding: 0 5px; }
</style>
