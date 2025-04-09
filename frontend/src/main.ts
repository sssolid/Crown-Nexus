import { createApp } from 'vue';
import { createPinia } from 'pinia';
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import router from '@/router';
import App from '@/App.vue';
import { i18n, initializeI18n } from '@/i18n';


// Import styles
import '@mdi/font/css/materialdesignicons.css';
import 'vuetify/styles';

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          // Primary brand color - deep blue with slight automotive tint
          primary: '#0B3D91',      // Distinctive dark blue for main elements

          // Secondary colors
          secondary: '#303640',    // Dark slate gray for headers/footers
          tertiary: '#D84315',     // Burnt orange for selective accents

          // Functional colors
          accent: '#5C8BC3',       // Medium blue for highlighting
          error: '#C62828',        // Deep red for errors/warnings
          info: '#1565C0',         // Informational blue
          success: '#2E7D32',      // Deep green for success states
          warning: '#EF6C00',      // Dark orange for warnings

          // UI background variations
          background: '#FFFFFF',   // Clean white background
          surface: '#F8F9FA',      // Very light gray for cards/surfaces
          'surface-variant': '#E8EAF0', // Light blue-gray for containers

          // Text colors
          'on-primary': '#FFFFFF',
          'on-secondary': '#FFFFFF',
          'on-surface': '#1E293B',  // Dark blue-gray for text
          'on-surface-variant': '#475569', // Medium blue-gray for secondary text

          // Extended palette for components
          'neutral-100': '#F1F5F9', // Lightest gray
          'neutral-200': '#E2E8F0', // Light gray for dividers
          'neutral-300': '#CBD5E1', // Medium light gray for borders
          'neutral-400': '#94A3B8', // Medium gray
          'neutral-500': '#64748B', // Medium gray text

          // Automotive-inspired accent colors
          'automotive-silver': '#C0C2C9', // Metallic silver
          'automotive-chrome': '#9BA0AA', // Chrome-inspired
          'automotive-race': '#D00000',   // Racing red for special elements
        },
        variables: {
          // Border radius for components
          'border-radius-root': '4px',
          'border-color': '#CBD5E1',

          // Shadow definitions for depth
          'box-shadow': '0 2px 4px rgba(15, 23, 42, 0.08)',
          'elevated-shadow': '0 4px 8px rgba(15, 23, 42, 0.12)',

          // Font related
          'font-family': '"Inter", "Roboto", sans-serif',
          'line-height-root': 1.5,

          // Opacity settings
          'high-emphasis-opacity': 0.9,
          'medium-emphasis-opacity': 0.7,
          'disabled-opacity': 0.38,

          // Transition speed
          'transition-fast-out-slow-in-timing-function': 'cubic-bezier(0.4, 0, 0.2, 1)',
          'transition-fast-out-linear-in-timing-function': 'cubic-bezier(0.4, 0, 1, 1)',
          'transition-linear-out-slow-in-timing-function': 'cubic-bezier(0, 0, 0.2, 1)',
          'transition-duration': '200ms',
        }
      },
      // Dark theme (optional)
      dark: {
        colors: {
          // Primary brand color remains recognizable
          primary: '#2673CE',      // Brighter blue for dark mode

          // Adjusted secondary colors for dark mode
          secondary: '#252A32',    // Slightly lighter dark gray
          tertiary: '#FF6E40',     // Brighter orange for dark mode

          // Functional colors - brighter for dark backgrounds
          accent: '#7BA7E1',       // Lighter blue for highlighting
          error: '#EF5350',        // Bright red for errors
          info: '#42A5F5',         // Brighter blue for information
          success: '#66BB6A',      // Bright green
          warning: '#FFA726',      // Bright orange

          // Dark theme backgrounds
          background: '#121212',   // Very dark background
          surface: '#1E1E1E',      // Dark gray surface
          'surface-variant': '#2C2C2C', // Slightly lighter surface

          // Text colors for dark theme
          'on-primary': '#FFFFFF',
          'on-secondary': '#FFFFFF',
          'on-surface': '#E2E8F0',
          'on-surface-variant': '#94A3B8',

          // Extended palette for dark theme
          'neutral-100': '#2C2C2C',
          'neutral-200': '#383838',
          'neutral-300': '#454545',
          'neutral-400': '#707070',
          'neutral-500': '#909090',

          // Automotive accents for dark theme
          'automotive-silver': '#D4D6DD',
          'automotive-chrome': '#B0B5C1',
          'automotive-race': '#FF4D4D',
        }
      }
    }
  },
  defaults: {
    // Component styling defaults
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
    }
  },
});

// Create app
const pinia = createPinia();
const app = createApp(App);

// Use plugins
app.use(pinia);
app.use(router);
app.use(i18n);
app.use(vuetify);

// Initialize i18n before mounting
initializeI18n().then(() => {
  // Mount app
  app.mount('#app')
})
