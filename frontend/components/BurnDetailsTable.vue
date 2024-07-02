<template>
  <div>
    <div class="table table--response mt-30">
      <div class="table__row table__row_header">
        <div class="row-item row-item--80">{{t('burn_details.table.title_1')}}</div>
        <div class="row-item row-item--100">%</div>
        <div class="row-item row-item--130">{{t('burn_details.table.title_3')}}</div>
        <div class="row-item row-item--130">{{t('burn_details.table.title_4')}}</div>
      </div>
      <div class="table-body table-body--pagination">
        <div
            :key="item._id"
            v-for="(item,index) in currentData"
            class="table__row table__row_body"
        >
          <div :data-title="t('burn_details.table.title_1')" :data-type="item.type" class="row-item row-item--80">
            <div class="coin-icon"><FOMO/></div>
            <div class="flex flex-column">
              <span>{{formatNumberToString(item.tokens_burned / 1e18)}}</span>
              <span class="mt-5 gray-color-200">${{formatNumberToString(item.tokens_burned_usd, 1000)}}</span>
            </div>
          </div>
          <div data-title="%" class="row-item row-item--100">
            {{ myToFixed((item.tokens_burned / 1e18) / totalSupply * 100, 4) }}%
          </div>
          <div :data-title="t('burn_details.table.title_3')" class="row-item row-item--130"
          >
            <div class="flex flex-column">
              <a
                  :href="`https://basescan.org/tx/${item.transaction_details}`"
                  target="_blank"
              >
                {{cropText(item.transaction_details)}}
              </a>
              <div class="fs-12 mt-5 gray-color-200">{{DateToRead(item.timestamp)}}</div>
            </div>
          </div>
          <div :data-title="t('burn_details.table.title_4')" class="row-item row-item--130">
            <a :href="`https://basescan.org/address/${item.burn_triggered_by}`" target="_blank">{{cropText(item.burn_triggered_by)}}</a>
          </div>
        </div>
      </div>
    </div>
    <div
        class="pagination__wrapper"
    >
      <vue-awesome-paginate
          :total-items="totalItems"
          :items-per-page="items_per_page"
          :modelValue="currentPageBurnDetails"
          @update:modelValue="updateCurrentPage"
          :hide-prev-next-when-ends="true"
          :show-breakpoint-buttons="true"
      />
    </div>
  </div>
</template>

<script setup>
import {VueAwesomePaginate} from "vue-awesome-paginate";
import {useMain} from "~/stores/main.js"
import FOMO from "~/components/UIComponents/Icons/FOMO.vue";
import {ref} from "vue";
const {t} = useI18n()

const {formatNumberToString, cropText, DateToRead, myToFixed} = useMain()
const props = defineProps({
  burn_details: {
    type: Array,
  },
  totalSupply: Number,
  currentPage: Number
})

const items_per_page = 5;
const currentPageBurnDetails = ref(props.currentPage);
const totalItems = computed(() => {
  return props.burn_details?.length || 0;
});

const emit = defineEmits(['update:currentPage']);
watch(() => props.currentPage, (newVal) => {
  currentPageBurnDetails.value = newVal;
});
const updateCurrentPage = (page) => {
  currentPageBurnDetails.value = page;
  emit('update:currentPage', page);
};

const paginatedData = computed(() => {
  if (!props.burn_details?.length) {
    return [];
  }
  // Количество элементов в массиве
  // Вычисление общего количества страниц
  const numberOfPages = Math.ceil(totalItems.value / items_per_page);

  // Создание массива страниц, каждая страница содержит до pageSize элементов
  return Array.from({ length: numberOfPages }, (v, i) => {
    // Вычисление начального индекса для каждой страницы
    const start = i * items_per_page;
    // Возвращаем срез массива для каждой страницы
    return props.burn_details?.slice(start, start + items_per_page);
  });
});

const currentData = computed(() => {
  return paginatedData.value[props.currentPage - 1] || [];
});

</script>