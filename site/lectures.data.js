// Список лекций для главной страницы — из файла, который пишет tools/slides2notes.py
import { readFileSync, existsSync } from 'node:fs'

const file = new URL('./.vitepress/lectures.json', import.meta.url)

export default {
  watch: ['./.vitepress/lectures.json'],
  load() {
    return existsSync(file) ? JSON.parse(readFileSync(file, 'utf-8')) : []
  },
}
