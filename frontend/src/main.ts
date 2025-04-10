import { createApp } from 'vue';
import { createPinia } from 'pinia';
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import router from '@/router';
import App from '@/App.vue';
import { i18n, initializeI18n } from '@/i18n';
import VueApexCharts from "vue3-apexcharts";
import globalComponents from '@/plugins/components'


// Import styles
import '@mdi/font/css/materialdesignicons.css';
import 'vuetify/styles';
import { lightTheme, darkTheme } from '@/theme'

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'dark',
    themes: {
      light: lightTheme,
      dark: darkTheme,
    },
  },
  defaults: {
    VBtn: {
      rounded: 'sm',
      elevation: '1',
      fontWeight: '500',
    },
    VCard: {
      rounded: 'sm',
      elevation: '1',
    },
    VAppBar: {
      elevation: '2',
    },
    VNavigationDrawer: {
      color: 'surface',
    },
    VTextField: {
      variant: 'outlined',
      density: 'comfortable',
    },
    VTable: {
      color: 'surface',
      density: 'comfortable',
    },
    VChip: {
      rounded: 'sm',
    },
    VTabs: {
      color: 'primary',
    },
  },
})

// Create app
const pinia = createPinia();
const app = createApp(App);

// Use plugins
app.use(pinia);
app.use(router);
app.use(i18n);
app.use(vuetify);
app.use(VueApexCharts);
app.use(globalComponents);

// Initialize i18n before mounting
initializeI18n().then(() => {
  // Mount app
  app.mount('#app')
})
