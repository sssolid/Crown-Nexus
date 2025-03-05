import { createApp } from 'vue';
import { createPinia } from 'pinia';
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import router from '@/router';
import App from '@/App.vue';

// Import styles
import '@mdi/font/css/materialdesignicons.css';
import 'vuetify/styles';

// Vuetify instance
const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#1976D2',
          secondary: '#424242',
          accent: '#82B1FF',
          error: '#FF5252',
          info: '#2196F3',
          success: '#4CAF50',
          warning: '#FB8C00',
        },
      },
    },
  },
});

// Create app
const app = createApp(App);

// Use plugins
app.use(createPinia());
app.use(router);
app.use(vuetify);

// Mount app
app.mount('#app');
