<template>
  <label class="custom-radio-button">
    <input type="radio" :name="nameInput" :value="nameInput" :checked="isChecked">
    <span class="checkmark"></span>
    {{nameInput}}
  </label>
</template>

<script setup>
const props = defineProps({
  nameInput: {
    type: String,
    required: true
  },
  isChecked: {
    type: Boolean,
    required: true
  }
})
</script>

<style lang="scss">
.custom-radio-button {
  display: flex;
  align-items: center;
  gap: 12px;
  input[type="radio"] {
    opacity: 0;
    position: fixed;
    width: 0;
  }

  .checkmark {
    position: relative;
    height: 25px;
    width: 25px;
    background-color: transparent;
    border-radius: 50%;
    display: inline-block;
    border: 2px solid $rose-color;

    &:after {
      content: "";
      position: absolute;
      display: none;
    }
  }

  input[type="radio"]:checked ~ .checkmark:after {
    display: block;
  }
  .checkmark:after {
    top: 50%;
    left: 50%;
    width: 15px;
    height: 15px;
    transform: translate(-50%, -50%);
    border-radius: 50%;
    background: $rose-color;
  }
}
</style>