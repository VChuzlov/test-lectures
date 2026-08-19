<!--
  Fig.vue — запасной способ вставки адаптивного графика.

  Нужен, если сгенерированный компонент почему-то не собирается: здесь SVG
  вставляется через v-html, то есть компилятор шаблонов Vue его вообще не разбирает,
  и никакие теги внутри SVG сломать сборку не могут. currentColor и var(--sN)
  при этом продолжают работать — SVG всё равно оказывается инлайновым в DOM.

  Использование в слайде:
      <Fig src="cp" />              (возьмёт ./pics/cp.svg)
      <Fig src="cp" class="w-[560px] mx-auto" />
-->
<script setup>
import { computed } from 'vue'

const props = defineProps({ src: { type: String, required: true } })

// Vite подставит содержимое всех SVG из pics/ на этапе сборки
const files = import.meta.glob('../pics/*.svg', {
  query: '?raw',
  import: 'default',
  eager: true,
})

const svg = computed(() => {
  const key = `../pics/${props.src}.svg`
  if (!files[key]) {
    console.warn(`[Fig] не найден ${key}. Доступны:`, Object.keys(files))
    return `<!-- не найден ${key} -->`
  }
  return files[key]
})
</script>

<template>
  <div class="fig-wrap" v-html="svg" />
</template>

<style scoped>
.fig-wrap :deep(svg) {
  width: 100%;
  height: auto;
}
</style>
