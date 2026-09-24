<!-- Аналог встроенного <LightOrDark> из Slidev. Рисуются обе версии,
     видимость переключает CSS по классу html.dark — без мигания при загрузке. -->
<template>
  <div class="lod">
    <div class="lod-light"><slot name="light" /></div>
    <div class="lod-dark"><slot name="dark" /></div>
  </div>
</template>

<style>
.lod-dark { display: none; }
html.dark .lod-dark { display: block; }
html.dark .lod-light { display: none; }
.lod img { margin: 0 auto; }
</style>
