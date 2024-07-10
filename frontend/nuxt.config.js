// https://nuxt.com/docs/api/configuration/nuxt-config

const publicWebUrl = "http://localhost:3000/";
import languages from './src/multiLang.config.json';
const defaultLocale = "en"

export default defineNuxtConfig({
  devtools: { enabled: true },
  googleFonts: {
    families: {
      Lato: [400, 700, 900],
      Montserrat: [100, 300, 400, 500, 600, 700, 800, 900]
    },
    display: 'swap',
    preconnect: true,
    preload: true,
  },
  modules: [
    '@pinia/nuxt',
    "@nuxtjs/google-fonts",
    '@nuxtjs/i18n'
  ],
  plugins: [
    '~/plugins/click-outside.js'
  ],
  i18n: {
    legacy: false,
    defaultLocale: defaultLocale,
    locale: defaultLocale,
    lazy: true,
    langDir: "locales/",
    locales: languages,
    strategy: "no_prefix",
    detectBrowserLanguage: {
      useCookie: true,
      cookieKey: 'i18n_redirected',
      alwaysRedirect: false,
      fallbackLocale: defaultLocale,
      redirectOn: 'root',
    }
  },
  vite:{
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: `
          @import "@/assets/styles/vars.scss";
        `
        }
      }
    }
  }
})
