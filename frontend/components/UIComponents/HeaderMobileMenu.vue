<template>
  <div v-if="state.burgerIsActive" class="mobile-menu" :class="state.burgerIsActive ? '_active' : ''">
    <HeaderNav/>
  </div>
</template>

<script setup>
import {useMain} from "~/stores/main.js";

const {state} = useMain();
</script>

<style lang="scss">
@media (max-width: 767px) {
  .mobile-menu {
    position: fixed;
    bottom: -100%;
    left: 0;
    width: 100%;
    height: 100%;
    border-top: 1px solid #3D3D5D;
    background: #0F0F38;
    padding: 30px;
    z-index: 1000;
    & .navigation-items{
      flex-direction: column;
      align-items: start;
    }
    &._active {
      top: 72px;
    }
  }
}
</style>