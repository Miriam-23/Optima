import { createApp } from "vue";
import App from "./App.vue";
import router from './router';
import { createPinia } from 'pinia'
import vuetify from "./plugins/vuetify";
import VueApexCharts from "vue3-apexcharts"
import { loadFonts } from "./plugins/webfontloader";

loadFonts();

createApp(App)
.use(createPinia())
.use(router)
.use(vuetify)
.use(VueApexCharts)
.mount("#app");

