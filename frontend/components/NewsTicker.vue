<template>
  <div class="news-ticker">
    <div class="container">
      <transition-group name="slide" tag="div" class="news-messages">
        <div v-for="(message, index) in messages" :key="index" v-show="index === currentIndex" class="news-message">
          {{ message }}
        </div>
      </transition-group>
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted, onUnmounted} from 'vue';

const props = defineProps({
  messages: {
    type: Array,
    required: true
  }
});

const currentIndex = ref(0);
let intervalId;

onMounted(() => {
  intervalId = setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % props.messages.length;
  }, 5000);
});

onUnmounted(() => {
  clearInterval(intervalId);
});
</script>

<style>
.news-ticker {
  position: relative;
  width: 100%;
  background: rgba(217, 0, 210, 0.15);
  color: white;
  overflow: hidden;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}

.news-message {
  position: absolute;
  width: 100%;
  text-align: center;
  white-space: nowrap;
  top: 50%;
  transform: translateY(-50%);
  left: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
}

.slide-enter-active, .slide-leave-active {
  transition: transform 1s ease, opacity .1s ease;
}

.slide-enter-from {
  transform: translateY(100%);
  opacity: 0;
}

.slide-enter-to {
  transform: translateY(-50%);
  opacity: 1;
}

.slide-leave-from {
  transform: translateY(-50%);
  opacity: 1;
}

.slide-leave-to {
  transform: translateY(-100%);
  opacity: 0;
}
</style>