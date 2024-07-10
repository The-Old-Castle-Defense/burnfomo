<template>
  <a
    class="btn btn--transparent btn--buy-fomo"
    href="https://app.debridge.finance/deswap?address=&inputChain=1&outputChain=8453&inputCurrency=&outputCurrency=0xa7ea9d5d4d4c7cF7dbde5871E6D108603C6942a5&dlnMode=simple"
    target="_blank"
  >
    {{t('buy_fomo')}}
  </a>
</template>

<script setup>
const {t} = useI18n()
</script>

<style lang="scss">
.btn {
  border-radius: 7px;
  padding: 12px 24px;
  cursor: pointer;
  transition: all 0.3s;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  width: max-content;
  font-weight: 700;
  font-size: 14px;
  position: relative;
  background: transparent;
  &--transparent {
    border: 1px solid $rose-color;
    &:hover {
      &:not([disabled]) {
        border: 1px solid $rose-color--hover;
        background: $rose-color--hover;
      }
    }
  }
}

@media (max-width: 567px){
  .btn--buy-fomo {
    padding: 12px 12px;
  }
}
</style>