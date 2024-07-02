<template>
  <NuxtLink to="/" class="logo">
    <img class="logo__logo" src="/logo.svg" alt="logo">
  </NuxtLink>
</template>

<style>
.logo{
  cursor: pointer;
  & img{
    width: 100%;
    height: 100%;
  }
}

@media (max-width: 400px) {
  .logo{
    max-width: 120px;
    max-height: 20px;
  }
}
</style>
