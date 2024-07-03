<template>
  <div>
    <Header/>
    <NewsTicker :messages="messagesNews" />
    <main class="super-section">
      <div class="container">
        <div class="board-wrapper board-wrapper--description">
          <FOMOBurnEmotion :last-burn="last_burn_details?.timestamp"/>
          <div class="board board--burn-description">
            <div class="board__header">
              {{t('total_burned.title')}}
              <span class="rose-color">{{myToFixed(totalBurnPercent)}}%</span>
            </div>
            <div class="board__body">
              {{t('total_burned.body', {totalBurnValue: myToFixed(total_burned_value), totalBurnValueInUSD:myToFixed(total_burned_value * fomoRate) , average_burn_size: myToFixed(average_burn_size) })}}
            </div>
            <div class="chart-container chart-container--doughnut">
              <Doughnut :options="chartOptionsDoughnut" :data="chartDataDoughnut" />
            </div>
          </div>
          <div class="board board--fomo-rate">
            <div class="board__header board__header--small">{{t('rate.title')}}</div>
            <div class="board__body">
              <div class="rate flex align-center">
                <FOMO/>
                {{myToFixed(fomoRate, 6)}}
              </div>
              <div class="rate_pair mb-30">
                FOMO/WETH
              </div>
            </div>
            <div class="board__bottom">
              {{t('rate.last_updated')}}: {{state.fetchRateLastUpdate === 0 ? 'a few seconds ago' : ` a ${state.fetchRateLastUpdate} minutes ago`}}
            </div>
          </div>
        </div>

        <div class="board-wrapper mt-20">
          <div class="board">
            <div class="board__header board__header--small">{{t('latest_burn_details.title')}}</div>
            <div class="board__header mt-10">{{t('latest_burn_details.subtitle')}}<br>
              <span class="rose-color">{{DateToRead(last_burn_details?.timestamp)}}</span>
            </div>
            <div class="board__body">
              {{t('latest_burn_details.body',
                {
                  totalTokensBurned: last_burn_details?.tokens_burned / 1e18,
                  totalTokensBurnedUSD: myToFixed(last_burn_details?.tokens_burned_usd, 6),
                }
              )}}
              <div class="mt-10">
                {{t('latest_burn_details.body2')}} <a :href="`https://basescan.org/address/${last_burn_details?.burn_triggered_by}`" target="_blank">{{cropText(last_burn_details?.burn_triggered_by)}}</a>
              </div>
            </div>
          </div>
          <div class="board">
            <div class="board__header board__header--small">
              {{t('line_chart.title')}}
            </div>
            <div class="chart-container chart-container--line mt-25">
              <Line :options="chartOptionsLine" :data="chartDataLine" />
            </div>
          </div>
        </div>

        <div class="board-wrapper board-wrapper--upcoming mt-20">
          <div class="board board--ETH">
            <div class="board__header board__header--small">{{t('upcoming_buybacks.title')}}</div>
            <div class="board__header mt-15">{{myToFixed(ETHBalance, 6)}} $ETH</div>
            <p class="gray-color-100 mt-10 fs-14">${{myToFixed(ETHBalance * ETHRate)}}</p>
            <div class="upcoming-image">
              <img src="/images/ETH.png" alt="Image">
            </div>
          </div>
          <div class="board board--FOMO">
            <div class="board__header board__header--small">{{t('upcoming_burns.title')}}</div>
            <div class="board__header mt-15">{{myToFixed(ERC20TokenBalance, 2)}} $FOMO</div>
            <p class="gray-color-100 mt-10 fs-14">${{myToFixed(ERC20TokenBalance * fomoRate)}}</p>
            <div class="upcoming-image">
              <img src="/images/FOMO.png" alt="Image">
            </div>
          </div>
        </div>

        <div class="board-wrapper board-wrapper--tables mt-20">
          <div class="board">
            <div class="board__header board__header--small">
              {{t('burn_details.title')}}
            </div>
            <BurnDetailsTable
                :burn_details="allStatistics?.burn_details"
                :totalSupply="totalSupply"
                :currentPage="currentPageBurnDetails"
                @update:currentPage="updateCurrentPage"
            />
          </div>
          <div class="board">
            <div class="board__header board__header--small">{{t('top_5_burn.title')}}</div>
            <Top5BurnTable
                :top_5_burn="allStatistics?.top_5_burn_triggered_by_wallets"
                :fomoRate="fomoRate"
            />
          </div>
        </div>
        <h2 class="title mt-65">{{t('burn_statistics.title')}}</h2>
        <div class="board-wrapper board-wrapper__burn-statistics mt-30">
          <div class="board">
            <div class="board__header board__header--small">
              {{t('burn_statistics.board_1.title')}}
            </div>
            <div class="board__body mb-30">
              <div class="rate flex align-center">
                <FOMO/>
                {{myToFixed(biggest_burn_value)}}
              </div>
              <p class="fs-14 gray-color-100 mt-10">
                ${{myToFixed(biggest_burn_value * fomoRate)}}
              </p>
            </div>
            <div class="board__bottom">
              {{DateToRead(biggest_burn?.date, true)}}
            </div>
          </div>
          <div class="board board--blue board--center">
            <div class="board__header board__header--small">{{t('burn_statistics.board_2.title')}}</div>
            <div class="board__body board__body--large board__body--white">
              {{allStatistics?.burn_statistics?.burns_to_date}}
            </div>
            <div class="board__bottom">
              {{t('burn_statistics.board_2.subtitle')}}
            </div>
          </div>
          <div class="board">
            <div class="board__header board__header--small">
              {{t('burn_statistics.board_3.title')}}
            </div>
            <div class="board__body mb-30">
              <div class="rate flex align-center">
                <FOMO/>
                {{myToFixed(average_burn_size)}}
              </div>
              <p class="fs-14 gray-color-100 mt-10">
                ${{myToFixed(average_burn_size * fomoRate)}}
              </p>
            </div>
          </div>
        </div>
        <div class="section mt-65" id="faq">
          <div class="title">{{t('faq.title')}}</div>
          <div class="accordion accordion--airdrop mt-30">
            <FAQ
                v-for="(item, index) in faqQuestions"
                :key="index"
                :id="item"
                :title_text="parseQuestion(item.question)"
                :content_text="parseQuestion(item.answer)"
            />
          </div>
        </div>
      </div>
    </main>
    <Footer/>
  </div>
</template>

<script setup>
import {useMain} from "~/stores/main";
import {ref} from 'vue'
import FOMO from "~/components/UIComponents/Icons/FOMO.vue";
import FOMOBurnEmotion from "~/components/FOMOBurnEmotion.vue";
import FAQ from "~/components/FAQ.vue";
import {Doughnut, Line} from 'vue-chartjs';

import {
  Chart as ChartJS,
  ArcElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    ArcElement,
    Filler
);

const needlePlugin = {
  id: 'needle',
  afterDatasetDraw: (chart) => {
    const needleValue = chart.config.options.needleValue;
    if (needleValue !== undefined) {
      const ctx = chart.ctx;
      const chartArea = chart.chartArea;
      const centerX = (chartArea.left + chartArea.right) / 2;
      const centerY = chartArea.bottom - 3; // Позиционируем стрелку чуть выше
      const angle = Math.PI + (Math.PI * needleValue / 100);
      const needleLength = (chartArea.right - chartArea.left) / 2.5;
      const needleWidth = 7;

      ctx.save();
      ctx.translate(centerX, centerY);
      ctx.rotate(angle);

      // Рисуем стрелку с округлым основанием снаружи
      ctx.beginPath();
      ctx.moveTo(0, -needleWidth / 2); // Левая нижняя точка стрелки
      ctx.lineTo(needleLength, 0); // Верхняя точка стрелки
      ctx.lineTo(0, needleWidth / 2); // Правая нижняя точка стрелки
      ctx.arc(0, 0, needleWidth / 2, Math.PI / 2, -Math.PI / 2, false); // Округлое основание стрелки снаружи
      ctx.fillStyle = 'rgba(213, 213, 220, 1)';
      ctx.fill();
      ctx.restore();
    }
  }
};



ChartJS.register(needlePlugin);

const {state, myToFixed, getBurnStatistics, getFOMORate, setCookie, DateToRead, formatNumberToString, cropText, getBalances, getETHRate} = useMain();
const {t, locale, messages} = useI18n()

const totalSupply = 100000000;
const fomoRate = ref(0)
const ETHRate = ref(0)
const ETHBalance = ref(0)
const ERC20TokenBalance = ref(0)
const allStatistics = ref([])

const currentPageBurnDetails = ref(1);
const updateCurrentPage = (page) => {
  currentPageBurnDetails.value = page;
};

const totalBurnPercent = computed(() => allStatistics.value?.total_fomo_supply_reduced)
const circulating_supply = computed(() => allStatistics.value?.circulating_supply / 1e18)
const total_burned_value = computed(() => totalSupply - circulating_supply.value)
const average_burn_size = computed(() => allStatistics.value?.burn_statistics?.average_burn_size / 1e18)
const last_burn_details = computed(() => allStatistics.value?.burn_details?.[0])
const biggest_burn = computed(() => allStatistics.value?.burn_statistics?.biggest_burn)
const biggest_burn_value = computed(() => biggest_burn.value?.amount / 1e18)

const burn_color = '#D900D2'
const supply_color = '#3B3390'


const chartOptionsDoughnut = computed(() => ({
  rotation: -90,
  circumference: 180,
  responsive: true,
  maintainAspectRatio: false,
  needleValue: totalBurnPercent.value,
  needle: true,
  plugins: {
    legend: {
      display: false
    }
  }
}));

const chartDataDoughnut = computed(() => ({
  labels: ['Burned', 'Circulating supply'],
  datasets: [{
    data: [total_burned_value.value, totalSupply - total_burned_value.value],
    backgroundColor: [burn_color, supply_color],
    hoverOffset: 0,
    borderColor: 'transparent',
    borderWidth: 0,
  }]
}));


const chartOptionsLine = {
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        callback: (value) => formatNumberToString(value, 1000, 0)
      }
    },
    x: {
      display: false
    },
  },
  elements: {
    line: {
      tension: 1
    },
    point: {
      radius: 0,
      hoverRadius: 0
    }
  },
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      enabled: true,
      mode: 'index',
      intersect: false,
      callbacks: {
        title: (tooltipItems) => {
          return `Supply: ${tooltipItems[0].raw.toLocaleString()}`;
        },
        label: (tooltipItem) => {
          return `Date: ${tooltipItem.label}`;
        }
      },
      displayColors: false
    }
  }
}

const chartDataLine = computed(() => ({
  labels: allStatistics.value?.fomo_total_supply_chart?.map(item => DateToRead(item.date, true)) || [],
  datasets: [{
    label: 'Supply',
    data: allStatistics.value?.fomo_total_supply_chart?.map(item => parseFloat(item.circulating_supply / 1e18)) || [],
    backgroundColor: 'rgba(92, 93, 151)',
    borderColor: 'rgb(92, 93, 151)',
    borderWidth: 1,
    fill: 'origin'
  }]
}));


const messagesNews = ref([
  'The more $FOMO you have — the less FOMO you have',
  'The more $FOMO you stake — the more $FOMO Points you get',
  'The more $FOMO you stake — the more $FOMO we burn',
  'The more $FOMO you stake — the more $FOMO value'
]);

onMounted(async () => {
  setCookie("timezone", new Date().getTimezoneOffset(), 360);
  allStatistics.value = await getBurnStatistics()
  fomoRate.value = await getFOMORate()
  ETHRate.value = await getETHRate()
  const [ethBalance, erc20Balance] = await getBalances();
  ETHBalance.value = ethBalance;
  ERC20TokenBalance.value = erc20Balance;
})


const faqQuestions = computed(() => {
  const currentLocale = locale.value;
  const questions = messages.value[currentLocale]?.faq?.questions;
  return Array.isArray(questions) ? questions : [];
});

function parseQuestion(question) {
  if (question.body?.static) {
    return question.body.static;
  }

  if (question.loc?.source) {
    return question.loc.source;
  }

  if (question.b?.s) {
    return question.b?.s;
  }

  return 'No question available';
}

const meta = {
  title: "🔥FOMO Burn Tracker",
  description: "Find out how much $FOMO is ready to get burned. Stay updated on future burns to see how they will affect the token supply and value.",
  image: "/SEO-banner.png"
}


useHead({
  title: meta.title,
  meta: [
    { name: 'description', content: meta.description },
    {property: 'og:title', content: meta.title},
    {property: 'og:description', content: meta.description},
    {property: 'og:image', content: meta.image},
    {name: 'twitter:title', content: meta.title},
    {name: 'twitter:description', content: meta.description},
    {name: 'twitter:image', content: meta.image}
  ],
})
</script>


<style lang="scss">
@import "assets/styles/reset";
@import "assets/styles/vars";
@import "assets/styles/app";
@import "assets/styles/pagination";
@import "assets/styles/table";
@import "assets/styles/faq";
</style>