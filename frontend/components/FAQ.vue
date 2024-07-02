<template>
  <div class="accordion-item">
    <button :class="['accordion-btn', {'_active': activeIndex}]" @click="toggleActive">
      <span class="accordion-title">{{title_text}}</span>
      <span class="icon"></span>
    </button>
    <div class="accordion-content" v-html="content_text"></div>
  </div>
</template>

<script setup>
import {ref} from "vue";

const props = defineProps({
  title_text: {
    type: String,
    default: ''
  },
  content_text: {
    type: String,
    default: ''
  }
})
const activeIndex = ref(false)
function toggleActive() {
  activeIndex.value = !activeIndex.value
}
</script>