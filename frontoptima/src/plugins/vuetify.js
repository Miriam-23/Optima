// STYLES
import "@mdi/font/css/materialdesignicons.css";
import "vuetify/styles";

// VUETIFY
import { createVuetify } from "vuetify";

const vuetify = createVuetify({
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        dark: false,
        colors: {
        background: '#ffffff',
        surface: '#f0f1f7',
        primary: '#0a0462',
        secondary: '#aec794',
        accent: '#0dc2d3',
        bubble: '#9ff1f8',
        success: '#09cd23',
        warning: '#fa7500',
        error: '#d81717',
        info: '#0084ff',
        efect: '#8e86ff'
      },
      },
      dark: {
        dark: true,
        colors: {
        background: '#010104',
        surface: '#101117',
        primary: '#6962b7',
        secondary: '#526b38',
        accent: '#2ce1f2',
        bubble: '#088d9a',
        success: '#5df064',
        warning: '#FFB74D',
        error: '#D50000',
        info: '#4FC3F7',
        efect: '#FFFFFF00'
      },
      },
    },
  },
  display: {
    mobileBreakpoint: 'sm',
    thresholds: {
      xs: 0,
      sm: 340,
      md: 540,
      lg: 800,
      xl: 1280,
    },
  },
})

export default vuetify