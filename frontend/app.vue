<template>
  <div>
    <Header/>
    <NuxtPage/>
    <Footer/>
  </div>
</template>

<script setup>
import {useMain} from "~/stores/main";
import languages from "~/src/multiLang.config.json";

const {getCookie, setCookie, state} = useMain();
const router = useRouter()
const route = useRoute()
const {setLocale} = useI18n()
const initLanguages = () => {
  if (typeof window === 'undefined') return;

  const routeLang = route.params.lang;
  const _selectedLanguage = languages.find((l) => l.code === routeLang);

  if (routeLang?.length && languages.some(lang => lang.code === routeLang)) {
    state.selectedLanguage = _selectedLanguage;
    router.push(routeLang);
    setLocale(routeLang);
  } else {
    let cookieLang = getCookie("i18n_redirected");
    router.push(cookieLang);
    setLocale(cookieLang);
  }
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
    {name: 'twitter:image', content: meta.image},
    {property: 'twitter:card', content: "summary_large_image"}
  ],
})
onMounted(() => {
  initLanguages()
})
</script>


<style lang="scss">
@import "assets/styles/reset";
@import "assets/styles/vars";
@import "assets/styles/app";
@import "assets/styles/pagination";
@import "assets/styles/table";
@import "assets/styles/faq";
@import "assets/styles/dropDownMenu";
</style>