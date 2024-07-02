<template>
  <div class="burger" :class="state.burgerIsActive ? '_active' : ''" @click="toggleBurger">
    <div class="line1"></div>
    <div class="line2"></div>
    <div class="line3"></div>
  </div>
</template>

<script setup>
import {useMain} from "~/stores/main.js";

const {state, toggleBurger} = useMain();

</script>

<style lang="scss">
@media (max-width: 767px) {
  .burger {
    width: 30px;
    height: 25px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    cursor: pointer;
    padding: 5px;
  }

  .burger div {
    width: 100%;
    height: 1px;
    background-color: white;
    transition: all 0.3s ease;
    border-radius: 10px;
  }

  ._active .line1 {
    transform: rotate(-45deg) translate(-5px, 5px);
  }

  ._active .line2 {
    opacity: 0;
  }

  ._active .line3 {
    transform: rotate(45deg) translate(-5px, -5px);
  }
}
</style>