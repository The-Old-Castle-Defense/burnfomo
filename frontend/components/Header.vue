<template>
  <header class="header-wrapper">
    <div class="container">
      <div class="header">
        <Logo/>
        <div class="header__right-side">
          <HeaderNav class="mobile-hidden"/>
          <BuyFomoButton/>
          <HeaderMobileMenu/>
          <Languages/>
          <Burger/>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>

import Burger from "~/components/UIComponents/Burger.vue";
import HeaderMobileMenu from "~/components/UIComponents/HeaderMobileMenu.vue";
import Languages from "~/components/UIComponents/Languages.vue";
</script>

<style lang="scss">
header.header-wrapper{
  background: #0F0F38;
  min-height: 72px;
  display: flex;
  align-items: center;
}
.header, .header__right-side{
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.header__right-side{
  gap: 30px;
}
@media (max-width: 767px) {
  .header__right-side{
    gap: 10px;
  }
}
</style>

