---
theme: default
title: Введение в Python для химиков-технологов
css: styles.css
---

<script setup>
import { isDark, toggleDark } from '@slidev/client'
</script>

<!-- Кнопка переключения темы в правом верхнем углу -->
<div class="absolute top-4 right-4 z-10">
  <button 
    @click="toggleDark()" 
    class="px-3 py-1.5 rounded-lg text-sm font-medium
           bg-gray-200 text-gray-800 
           dark:bg-gray-700 dark:text-gray-200
           hover:bg-gray-300 dark:hover:bg-gray-600
           transition-colors duration-200"
  >
    <span v-if="isDark">☀️ Светлая тема</span>
    <span v-else>🌙 Тёмная тема</span>
  </button>
</div>

---
layout: center
---

# Основы программирования
## Python для химиков-технологов

Лекция 1: Введение

<div class="text-sm text-gray-500 dark:text-gray-400 mt-8">
  Кафедра химической технологии • 2026
</div>

---
layout: default
---

# Почему Python?

Химик-технолог в современном мире — это не только колбы и реакторы.

<div class="grid grid-cols-2 gap-4 mt-8">
<div>

- 📊 Обработка экспериментальных данных
- 📈 Визуализация результатов
- 🧪 Моделирование химических процессов
- 🤖 Машинное обучение в материаловедении

</div>
<div>

```python
# Пример: расчёт выхода реакции
R = 8.314  # Дж/(моль·К)
T = 500    # K
Ea = 75000 # Дж/моль

k = A * np.exp(-Ea / (R * T))
print(f"Константа скорости: {k:.4f}")
```

</div> </div>

---
layout: default
---

Структура курса
<div class="grid grid-cols-2 gap-8 mt-12"> <div>
Семестр 1
Основы Python

Типы данных и переменные

Условные операторы и циклы

Функции и модули

Работа с файлами

Библиотеки NumPy и Matplotlib

</div> <div>
Семестр 2
Прикладные инструменты

SciPy для инженерных расчётов

Pandas для обработки данных

RDKit для хемоинформатики

Основы машинного обучения

Итоговый проект

</div> </div>


---
layout: center
---

# Вопросы?


> **Важно:** в начале файла указан `css: styles.css` — это ссылка на наш файл со стилями, который лежит рядом.

---

## Файл 4: `lectures/01-intro/styles.css`

Здесь мы определим переменные для светлой и тёмной тем, а также стили для графиков, таблиц и блоков кода.

```css
/* ============================================
   СВЕТЛАЯ ТЕМА (по умолчанию)
   ============================================ */

:root {
  /* Фон слайда */
  --slidev-slide-background: #ffffff;
  --slidev-slide-color: #1a1a2e;

  /* Заголовки */
  --slidev-heading-color: #16213e;

  /* Блоки кода */
  --slidev-code-background: #f4f4f5;
  --slidev-code-color: #2d2d2d;
  --slidev-code-border: #e4e4e7;

  /* Таблицы */
  --slidev-table-background: #fafafa;
  --slidev-table-border: #d4d4d8;
  --slidev-table-header-background: #e4e4e7;

  /* Цитаты, блоки с информацией */
  --slidev-block-background: #f0f9ff;
  --slidev-block-border: #bae6fd;

  /* Ссылки */
  --slidev-link-color: #2563eb;

  /* Графики: если вставляете как SVG, эти переменные можно использовать */
  --plot-background: #ffffff;
  --plot-grid: #e5e7eb;
  --plot-text: #1f2937;
}

/* ============================================
   ТЁМНАЯ ТЕМА (html.dark)
   ============================================ */

html.dark {
  --slidev-slide-background: #0f172a;
  --slidev-slide-color: #e2e8f0;

  --slidev-heading-color: #f1f5f9;

  --slidev-code-background: #1e293b;
  --slidev-code-color: #e2e8f0;
  --slidev-code-border: #334155;

  --slidev-table-background: #1e293b;
  --slidev-table-border: #475569;
  --slidev-table-header-background: #334155;

  --slidev-block-background: #172554;
  --slidev-block-border: #3b82f6;

  --slidev-link-color: #60a5fa;

  --plot-background: #0f172a;
  --plot-grid: #334155;
  --plot-text: #e2e8f0;
}

/* ============================================
   ДОПОЛНИТЕЛЬНЫЕ СТИЛИ
   ============================================ */

/* Таблицы: используем переменные */
table {
  background-color: var(--slidev-table-background);
  border-color: var(--slidev-table-border);
}

thead {
  background-color: var(--slidev-table-header-background);
}

/* Блоки с информацией (компонент Note в Slidev) */
.block {
  background-color: var(--slidev-block-background);
  border-left: 4px solid var(--slidev-block-border);
}

/* Кнопка копирования кода (встроенный компонент Slidev) */
.slidev-code-copy {
  opacity: 0.7;
}

.slidev-code-copy:hover {
  opacity: 1;
}
```
