<template>
  <div class="table table--response mt-30">
    <div class="table__row table__row_header">
      <div class="row-item row-item--30">#</div>
      <div class="row-item row-item--100">{{t('top_5_burn.table.title_2')}}</div>
      <div class="row-item row-item--60">{{t('top_5_burn.table.title_3')}}</div>
      <div class="row-item row-item--100">{{t('top_5_burn.table.title_4')}}</div>
      <div class="row-item row-item--100">{{t('top_5_burn.table.title_5')}}</div>
    </div>
    <div class="table-body table-body--pagination">
      <div
          :key="item._id"
          v-for="(item,index) in top_5_burn"
          class="table__row table__row_body"
      >
        <div data-title="#" class="row-item row-item--30">
          <span v-if="index + 1 <= 3" class="rank" :class="[index + 1 === 1 ? 'rank--1' : index + 1 === 2 ? 'rank--2' : index + 1 === 3 ? 'rank--3': '']"></span>
          <span v-else>{{index + 1}}</span>
        </div>
        <div :data-title="t('top_5_burn.table.title_2')" class="row-item row-item--100">
          <a :href="`https://basescan.org/address/${item._id}`" target="_blank">{{cropText(item._id)}}</a>
        </div>
        <div :data-title="t('top_5_burn.table.title_3')" class="row-item row-item--60">
          {{item.burn_count}}
        </div>
        <div :data-title="t('top_5_burn.table.title_4')" class="row-item row-item--100">
          ${{formatNumberToString((item.total_burned / 1e18) * fomoRate)}}
        </div>
        <div :data-title="t('top_5_burn.table.title_5')" class="row-item row-item--100">
          <div class="flex align-center">
            <div class="coin-icon"><FOMO/></div>
            {{formatNumberToString(item.total_burned / 1e18)}}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {useMain} from "~/stores/main.js"
import FOMO from "~/components/UIComponents/Icons/FOMO.vue";

const {t} = useI18n()

const {cropText, formatNumberToString} = useMain()
const props = defineProps({
  top_5_burn: {
    type: Array,
  },
  fomoRate: Number
})
</script>