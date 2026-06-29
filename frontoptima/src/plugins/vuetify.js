// STYLES
import "@mdi/font/css/materialdesignicons.css";
import "vuetify/styles";

// VUETIFY
import { createVuetify } from "vuetify";

// COLORES
// Azul principal #2563EB
// Azul claro #60A5FA
// Gris muy claro #F8FAFC
// Gris oscuro #334155

// Recursos gráficos del sistema:
// ✅ Logo de OptimaPM.
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
        background: '#FFFFFF',
        surface: '#FAFAFA',
        primary: '#0a0461',
        secondary: '#01d0ff',
        accent: '#777777',
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
        background: '#000000',
        surface: '#0A0A0A',
        primary: '#0A0A0A',
        secondary: '#212121',
        accent: '#83d5fb',
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