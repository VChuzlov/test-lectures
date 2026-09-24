import { defineConfig } from 'vitepress'
import { readFileSync, existsSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import UnoCSS from 'unocss/vite'
import { presetWind3 } from 'unocss'

// Список лекций пишет tools/slides2notes.py (из шапок slides.md)
const listFile = fileURLToPath(new URL('./lectures.json', import.meta.url))
const lectures: { folder: string; lecture: string; title: string; slides: string }[] =
  existsSync(listFile) ? JSON.parse(readFileSync(listFile, 'utf-8')) : []

export default defineConfig({
  lang: 'ru-RU',
  title: 'Основы программирования',
  description: 'Конспекты лекций по Python для химиков-технологов',
  base: process.env.SITE_BASE || '/',
  cleanUrls: true,
  lastUpdated: true,
  appearance: true,                     // авто по системе + переключатель

  markdown: {
    math: true,                         // $…$ и $$…$$, как в Slidev
    theme: { light: 'github-light', dark: 'github-dark' },
    container: {
      tipLabel: 'Совет', warningLabel: 'Внимание', dangerLabel: 'Ошибка',
      infoLabel: 'Информация', detailsLabel: 'Подробнее',
    },
  },

  vite: {
    // те же утилитарные классы, что в слайдах (text-[var(--brand)], mx-auto, …)
    plugins: [UnoCSS({ presets: [presetWind3({ preflight: false })] })],
    server: { fs: { allow: ['..'] } },
  },

  themeConfig: {
    nav: [
      { text: 'Конспекты', link: lectures.length ? `/konspekt/${lectures[0].folder}/` : '/' },
    ],
    sidebar: [
      {
        text: 'Лекции',
        items: lectures.map(l => ({
          text: `${l.lecture}. ${l.title}`,
          link: `/konspekt/${l.folder}/`,
        })),
      },
    ],
    outline: { level: [2, 3], label: 'На этой странице' },
    docFooter: { prev: 'Предыдущая лекция', next: 'Следующая лекция' },
    lastUpdated: { text: 'Обновлено' },
    darkModeSwitchLabel: 'Тема',
    lightModeSwitchTitle: 'Светлая тема',
    darkModeSwitchTitle: 'Тёмная тема',
    sidebarMenuLabel: 'Лекции',
    returnToTopLabel: 'Наверх',
    notFound: { title: 'Страница не найдена', linkText: 'На главную', quote: '' },
    search: {
      provider: 'local',
      options: {
        translations: {
          button: { buttonText: 'Поиск', buttonAriaLabel: 'Поиск' },
          modal: {
            noResultsText: 'Ничего не найдено по запросу',
            resetButtonTitle: 'Сбросить',
            displayDetails: 'Подробный список',
            footer: { selectText: 'выбрать', navigateText: 'перейти', closeText: 'закрыть' },
          },
        },
      },
    },
    footer: { message: 'ОХИ ИШПР ТПУ · Основы программирования, 2026/27' },
  },
})
