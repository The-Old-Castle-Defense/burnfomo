<template>
  <label class="custom-checkbox">
    <input type="checkbox" class="hidden-checkbox" :data-enable="isChecked">
    <span class="checkbox"></span>
    {{text}}
  </label>
</template>

<script setup>
const props = defineProps({
  text: {
    type: String,
    default:''
  },
  isChecked: {
    type: Boolean,
    default: false
  }
})


</script>

<style lang="scss">
.checkbox-btn-wrapper {
  display: flex;
  margin-top: 40px;
  align-items: center;
  justify-content: space-between;
  & .custom-checkbox {
    width: auto;
  }
  &--justify-start {
    justify-content: flex-start;
  }
}
.checkbox-btn__items{
  display: flex;
  align-items: center;
  gap: 10px;
  &--scroll{
    overflow: auto;
    & div{
      flex:  0 0 auto;
    }
  }
}

.hidden-checkbox {
  -webkit-appearance: none;
  position: absolute;
  opacity: 0
}
.custom-checkbox .checkbox {
  width: 20px;
  height: 20px;
  border-radius: 4px;
  border: 1px solid rgba(255,255,255,.5);
  margin-right: 5px;
  position: relative;

}
.custom-checkbox {
  padding: 5px;
  display: flex;
  align-items: center;
  cursor: pointer;
  max-width: max-content;
  font-size: 14px;
  font-weight: 400;
}

.custom-checkbox .checkmark {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%,-50%);
  max-width: 70%;
  height: auto;
  display: none
}

.custom-checkbox input[data-enable="true"] + .checkbox .checkmark {
  display: block;
}

.custom-checkbox input[data-enable="true"] + .checkbox {
  background: $rose-color url('/assets/images/icons/checkmark.svg') no-repeat center;
  border: 1px solid $rose-color;
}

@media (max-width: 567px){
  .checkbox-btn-wrapper {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
    & .checkbox-btn__items--scroll{
      padding-bottom: 20px;
    }
  }
}

</style>