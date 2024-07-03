// https://nuxt.com/docs/api/configuration/nuxt-config

const publicWebUrl = "http://localhost:3000/";

const locales = [
  { code: 'en', iso: 'en-US', file: 'en.json' }
]

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
  i18n: {
    legacy: false,
    defaultLocale: "en",
    locale: "en",
    lazy: true,
    langDir: "locales/",
    locales: locales,
    strategy: "no_prefix",
    // detectBrowserLanguage: {
    //   useCookie: true,
    //   cookieKey: 'i18n_redirected',
    //   alwaysRedirect: false,
    //   fallbackLocale: "en"
    // }
    detectBrowserLanguage: false

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
