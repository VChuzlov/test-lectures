import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'
import 'virtual:uno.css'
import '../../../shared/style.css'   // та же тема, что у слайдов: токены и классы
import './notes.css'                 // как эти токены ложатся на страницу-конспект
import LightOrDark from './LightOrDark.vue'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('LightOrDark', LightOrDark)
  },
} satisfies Theme
