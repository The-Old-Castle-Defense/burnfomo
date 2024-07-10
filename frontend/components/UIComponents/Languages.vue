<template>
  <div class="dropdown-btn-wrapper" v-click-outside="onClickOutside">
    <button @click="toggleDropdown" class="dropdown-btn">
      <img :src="`/images/languages/${state.selectedLanguage.image}`" :alt="state.selectedLanguage.name" class="flag-icon" />
    </button>
    <div v-if="isDropdownOpen" class="dropdown-menu">
      <button
          v-for="language in languages"
          :key="language.name"
          class="dropdown-item"
          :class="{ active: state.selectedLanguage.name === language.name }"
          :disabled="state.selectedLanguage.name === language.name"
          @click="selectLanguage(language)">
        <img :src="`/images/languages/${language.image}`" :alt="language.name" class="flag-icon" />
        <span class="dropdown-item__name">{{ language.name }}</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import {useMain} from "~/stores/main";
import {ref} from 'vue';
import languages from "~/src/multiLang.config.json";

const router = useRouter()
const {getCookie, state} = useMain();
const {setLocale} = useI18n()

const isDropdownOpen = ref(false);

const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value;
};

const onClickOutside = () => {
  isDropdownOpen.value = false;
};

const selectLanguage = (language) => {
  state.selectedLanguage = language;
  isDropdownOpen.value = false;
  setLocale(language.code);
  router.push(language.code);
};

onMounted(() => {
  let _selectedLanguage = getCookie('i18n_redirected')
  _selectedLanguage = languages.find((l) => l.code === _selectedLanguage)
  state.selectedLanguage = _selectedLanguage
})
</script>

