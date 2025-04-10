// src/theme/index.ts
import { ThemeDefinition } from 'vuetify'

// Core design tokens
export const lightTheme: ThemeDefinition = {
  colors: {
    primary: '#0B3D91',
    secondary: '#303640',
    tertiary: '#D84315',
    accent: '#5C8BC3',
    error: '#C62828',
    info: '#1565C0',
    success: '#2E7D32',
    warning: '#EF6C00',

    // Surface colors
    background: '#FFFFFF',
    surface: '#F8F9FA',
    'surface-variant': '#E8EAF0',

    // On colors (text/icons on surfaces)
    'on-primary': '#FFFFFF',
    'on-secondary': '#FFFFFF',
    'on-surface': '#1E293B',
    'on-surface-variant': '#475569',

    // Neutral palette (for various UI elements)
    'neutral-100': '#F1F5F9',
    'neutral-200': '#E2E8F0',
    'neutral-300': '#CBD5E1',
    'neutral-400': '#94A3B8',
    'neutral-500': '#64748B',

    // Domain-specific colors
    'automotive-silver': '#C0C2C9',
    'automotive-chrome': '#9BA0AA',
    'automotive-race': '#D00000',
  }
}

export const darkTheme: ThemeDefinition = {
  colors: {
    primary: '#2673CE',
    secondary: '#252A32',
    tertiary: '#FF6E40',
    accent: '#7BA7E1',
    error: '#EF5350',
    info: '#42A5F5',
    success: '#66BB6A',
    warning: '#FFA726',

    // Surface colors
    background: '#121212',
    surface: '#1E1E1E',
    'surface-variant': '#2C2C2C',

    // On colors
    'on-primary': '#FFFFFF',
    'on-secondary': '#FFFFFF',
    'on-surface': '#E2E8F0',
    'on-surface-variant': '#94A3B8',

    // Neutral palette
    'neutral-100': '#2C2C2C',
    'neutral-200': '#383838',
    'neutral-300': '#454545',
    'neutral-400': '#707070',
    'neutral-500': '#909090',

    // Domain-specific colors
    'automotive-silver': '#D4D6DD',
    'automotive-chrome': '#B0B5C1',
    'automotive-race': '#FF4D4D',
  }
}

// Typography scale
export const typography = {
  fontFamily: 'Inter, Roboto, sans-serif',
  fontWeights: {
    light: 300,
    regular: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
  },
  sizes: {
    xs: '0.75rem',    // 12px
    sm: '0.875rem',   // 14px
    base: '1rem',     // 16px
    lg: '1.125rem',   // 18px
    xl: '1.25rem',    // 20px
    '2xl': '1.5rem',  // 24px
    '3xl': '1.875rem', // 30px
    '4xl': '2.25rem',  // 36px
    '5xl': '3rem',     // 48px
  },
  lineHeights: {
    tight: 1.25,
    normal: 1.5,
    relaxed: 1.75,
  }
}

// Spacing system
export const spacing = {
  0: '0',
  1: '0.25rem',  // 4px
  2: '0.5rem',   // 8px
  3: '0.75rem',  // 12px
  4: '1rem',     // 16px
  5: '1.25rem',  // 20px
  6: '1.5rem',   // 24px
  8: '2rem',     // 32px
  10: '2.5rem',  // 40px
  12: '3rem',    // 48px
  16: '4rem',    // 64px
}

// Border radius
export const borderRadius = {
  'none': '0',
  'sm': '0.125rem',   // 2px
  'DEFAULT': '0.25rem', // 4px
  'md': '0.375rem',   // 6px
  'lg': '0.5rem',     // 8px
  'xl': '0.75rem',    // 12px
  '2xl': '1rem',      // 16px
  'full': '9999px',
}

// Shadows
export const shadows = {
  sm: '0 1px 2px rgba(0, 0, 0, 0.05)',
  DEFAULT: '0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06)',
  md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
  lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
  xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
}

// Transitions
export const transitions = {
  fast: '150ms',
  normal: '250ms',
  slow: '350ms',
  easing: {
    ease: 'cubic-bezier(0.4, 0, 0.2, 1)',
    easeIn: 'cubic-bezier(0.4, 0, 1, 1)',
    easeOut: 'cubic-bezier(0, 0, 0.2, 1)',
  }
}

export default {
  lightTheme,
  darkTheme,
  typography,
  spacing,
  borderRadius,
  shadows,
  transitions
}
