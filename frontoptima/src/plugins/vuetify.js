// STYLES
import "@mdi/font/css/materialdesignicons.css";
import "vuetify/styles";

// VUETIFY
import { createVuetify } from "vuetify";

// Recursos gráficos del sistema:
// ✅ Logo de Optima.
// ✅ Ilustración para el login.
// ✅ Paleta de colores.
// ✅ Tipografía.
// ✅ Estilo de botones.
// ✅ Tarjetas.
// ✅ Iconografía.

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
        success: '#09cd23',
        warning: '#fa7500',
        error: '#d81717',
        info: '#0084ff',
        efect: '#FFFFFF00'
      },
      },
      dark: {
        dark: true,
        colors: {
        background: '#010104',
        surface: '#101117',
        primary: '#a39dfb',
        secondary: '#526b38',
        accent: '#2ce1f2',
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