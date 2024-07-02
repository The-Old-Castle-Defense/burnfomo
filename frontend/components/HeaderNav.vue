<template>
  <nav class="navigation-items">
    <a class="navigation-item" @click="scrollToElement('faq')">
      {{ t('header.faq') }}
    </a>
    <a class="navigation-item" href="https://theoldcastle.xyz/" target="_blank">
      {{ t('header.game') }}
      <OpenInNew/>
    </a>
  </nav>
</template>

<script setup>
const {t} = useI18n()
import {useMain} from "~/stores/main.js"

const {scrollToElement} = useMain()
</script>

<style lang="scss">
.navigation-items{
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 24px;
}
.navigation-item{
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  font-weight: 600;
  color: #fff;
  text-decoration: none;
}
</style>