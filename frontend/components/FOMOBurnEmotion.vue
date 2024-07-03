<template>
  <div class="board board--image">
    <img :src="`/images/burn_states/burn_fomo_${emotionNumber}.png`" alt="Burn Fomo">
    <div class="make-happy" @click="toggleBoardVisible">
      {{t('fomo_burn_emotion.make_happy')}}
      <div class="make-happy__board" :class="boardIsVisible ? '_active' : ''" @click.stop>
        <div class="triangle"></div>
        <div>
          {{t('fomo_burn_emotion.make_happy_board_part_1')}}
          <a href="https://theoldcastle.xyz/" target="_blank">
            {{t('fomo_burn_emotion.make_happy_board_part_2')}}
          </a>
          {{t('fomo_burn_emotion.make_happy_board_part_3')}}
        </div>
        <div class="closed" @click="boardIsVisible = false"><Close/></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Close from "~/components/UIComponents/Icons/Close.vue";
import {ref} from "vue"
const props = defineProps({
  lastBurn: {
    type: Number,
    required: true
  }
})

const boardIsVisible = ref(false)

const toggleBoardVisible = () => {
  console.log('boardIsVisible', boardIsVisible.value)
  boardIsVisible.value = !boardIsVisible.value
}

const {t} = useI18n()

const emotionsCount = 6;
const hoursInDay = 7 * 24;
const emotionInterval = hoursInDay / emotionsCount;

const emotionNumber = computed(() => {
  const currentTime = Date.now() / 1000;
  const hoursSinceLastBurn = (currentTime - props.lastBurn) / 3600;

  let currentEmotion = Math.floor(hoursSinceLastBurn / emotionInterval) % emotionsCount;

  currentEmotion = Math.max(emotionsCount - 1 - currentEmotion, 0);
  return currentEmotion;
});
</script>

<style lang="scss">
.make-happy {
  position: absolute;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  text-decoration: underline;
  transition: .2s;
  z-index: 1;
  &:hover{
    text-decoration: none;
  }
}

.make-happy__board{
  display: none;
  position: absolute;
  border-radius: 4px;
  background: #FFF;
  padding: 12px 16px;
  align-items: center;
  height: max-content;
  width: 330px;
  color: #0F0F38;
  left: -70px;
  font-size: 12px;
  font-weight: 400;
  bottom: calc(100% + 15px);
  & a{
    color: $rose-color;
  }
  &._active{
    display: flex;
  }
}
.triangle {
  width: 0;
  height: 0;
  border-left: 8px solid transparent;
  border-right: 8px solid transparent;
  border-top: 8px solid #fff;
  position: absolute;
  bottom: -6px;
  left: 95px;
}

@media (max-width: 1150px) {
  .make-happy__board, .triangle{
    left: 50%;
    transform: translateX(-50%);
  }
}
</style>