<template>
  <div class="dashboard">
    <div v-if="loading" class="dashboard__loader">
      <v-progress-circular indeterminate color="primary" size="48" width="3" />
    </div>

    <div v-else class="dashboard__content">
      <!-- Header -->
      <div class="dashboard__header">
        <div>
          <span class="eyebrow">Panel de control</span>
          <h1 class="dashboard__title">Dashboard General</h1>
        </div>
        <v-chip color="primary" variant="tonal" size="small" class="role-chip">
          {{ reportData?.rol }}
        </v-chip>
      </div>

      <!-- Stat cards: grid uniforme, no v-col con fracciones raras -->
      <div class="stats-grid">
        <div class="stat-card" v-for="(item, i) in statsCards" :key="i">
          <div class="stat-card__icon" :style="{ background: iconBg(item.color) }">
            <v-icon :color="item.color" size="22">{{ item.icon }}</v-icon>
          </div>
          <div class="stat-card__body">
            <h3 class="stat-card__value">{{ item.value }}</h3>
            <p class="stat-card__label">{{ item.title }}</p>
          </div>
        </div>
      </div>

      <!-- Charts -->
      <v-row class="section-row" dense>
        <v-col cols="12" md="8">
          <section class="panel">
            <header class="panel__header">
              <h2 class="panel__title">Progreso de proyectos</h2>
              <span class="panel__subtitle">% de tareas completadas por proyecto</span>
            </header>
            <apexchart
              v-if="series[0].data.length > 0"
              type="bar"
              height="300"
              :options="chartOptions"
              :series="series"
            />
            <div v-else class="empty-state">No hay proyectos activos para mostrar.</div>
          </section>
        </v-col>

        <v-col cols="12" md="4">
          <section class="panel">
            <header class="panel__header">
              <h2 class="panel__title">Estado de tareas</h2>
              <span class="panel__subtitle">Distribución global</span>
            </header>
            <apexchart
              v-if="donutSeries.reduce((a, b) => a + b, 0) > 0"
              type="donut"
              height="300"
              :options="donutOptions"
              :series="donutSeries"
            />
            <div v-else class="empty-state">Sin tareas registradas.</div>
          </section>
        </v-col>
      </v-row>

      <!-- Tareas críticas -->
      <v-row class="section-row">
        <v-col cols="12">
          <section class="panel">
            <header class="panel__header">
              <h2 class="panel__title">Tareas pendientes críticas</h2>
              <span class="panel__subtitle">Requieren atención inmediata</span>
            </header>

            <ul v-if="tareasPendientes.length > 0" class="task-list">
              <li v-for="t in tareasPendientes" :key="t.id" class="task-item">
                <span class="task-item__priority-bar" :class="`bar--${prioridadColor(t.prioridad)}`" />

                <v-icon :color="prioridadColor(t.prioridad)" size="20" class="task-item__icon">
                  mdi-alert-circle
                </v-icon>

                <div class="task-item__body">
                  <p class="task-item__title">{{ t.titulo }}</p>
                  <p class="task-item__meta">
                    <span class="task-item__project">{{ t.proyecto__nombre }}</span>
                    <span class="dot">·</span>
                    <span>Límite: {{ t.fecha_limite }}</span>
                  </p>
                </div>

                <v-chip :color="prioridadColor(t.prioridad)" variant="tonal" size="small" class="text-capitalize">
                  {{ t.prioridad }}
                </v-chip>
              </li>
            </ul>

            <div v-else class="empty-state empty-state--success">
              <v-icon color="success" size="28" class="mb-2">mdi-check-circle-outline</v-icon>
              <p>¡Felicidades! No tienes tareas críticas pendientes.</p>
            </div>
          </section>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import reportesService from '@/services/reportes'
import { useTheme } from 'vuetify'

const theme = useTheme()
const loading = ref(true)
const reportData = ref(null)

onMounted(async () => {
  try {
    const response = await reportesService.getGlobales()
    console.log(response.data)
    reportData.value = response.data
  } catch (error) {
    console.error('Error al conectar con la API de reportes:', error)
  } finally {
    loading.value = false
  }
})

/* ==========================================
   MAPPING DE KPIS (TARJETAS)
========================================== */
const statsCards = computed(() => {
  if (!reportData.value) return []
  const t = reportData.value.tarjetas
  return [
    { title: 'Proyectos activos', value: t.proyectos_activos, icon: 'mdi-folder-outline', color: 'primary' },
    { title: 'Total tareas', value: t.total_tareas, icon: 'mdi-format-list-checkbox', color: 'info' },
    { title: 'Completadas', value: t.completadas, icon: 'mdi-check-circle-outline', color: 'success' },
    { title: 'En progreso', value: t.en_progreso, icon: 'mdi-progress-clock', color: 'warning' },
    { title: 'Pendientes', value: t.pendientes, icon: 'mdi-alert-circle-outline', color: 'error' }
  ]
})

// Fondo suave para el ícono de cada tarjeta (deriva del color del tema)
const iconBg = (colorName) => {
  const c = theme.current.value.colors[colorName] || theme.current.value.colors.primary
  return `${c}1A` // ~10% opacidad en hex
}

/* ==========================================
   CONFIGURACIÓN DE GRÁFICA DE BARRAS
========================================== */
const barColors = computed(() => {
  const c = theme.current.value.colors

  const palette = [
    c.primary,
    c.accent,
    c.secondary,
    c.success,
    c.warning,
    c.info,
    c.error
  ]

  return reportData.value
  ? reportData.value.grafica_barras.map((_, i) => palette[i % palette.length])
  : []
})

const series = computed(() => {
  if (!reportData.value) return [{ name: 'Progreso', data: [] }]
  const porcentajes = reportData.value.grafica_barras.map(b => {
    if (b.total === 0) return 0
    return Math.round((b.completadas / b.total) * 100)
  })
  return [{ name: 'Progreso', data: porcentajes }]
})

const chartOptions = computed(() => {
  const categories = reportData.value ? reportData.value.grafica_barras.map(b => b.proyecto) : []
  const c = theme.current.value.colors

  return {
    chart: { 
      toolbar: { show: false },
      fontFamily: 'inherit',
      foreColor: c['on-surface'] 
    },
    plotOptions: { 
      bar: { 
        borderRadius: 6, 
        columnWidth: '45%',
        distributed: true 
      }
    },
    theme: {
      mode: theme.global.name.value
    },
    xaxis: {
      categories,
      labels: { 
        style: { 
          colors: c['on-surface'], 
          fontSize: '12px' 
        } 
      },
      axisBorder: { show: false },
      axisTicks: { show: false }
    },

    yaxis: {
      min: 0,
      max: 100,
      labels: { formatter: val => `${val}%`, style: { colors: c['on-surface'] } }
    },

    grid: { borderColor: `${c['on-surface']}1A`, strokeDashArray: 4 },
    dataLabels: { enabled: true, formatter: val => `${val}%`, style: { fontWeight: 600 } },
    colors: barColors.value
  }
})

/* ==========================================
   CONFIGURACIÓN DE GRÁFICA DE DONA
========================================== */
const donutSeries = computed(() => {
  if (!reportData.value) return [0, 0, 0, 0]
  const gd = reportData.value.grafica_dona
  return [gd.completadas, gd.en_progreso, gd.pendientes, gd.vencidas]
})

const donutOptions = computed(() => {
  const c = theme.current.value.colors
  return {
    labels: ['Completadas', 'En progreso', 'Pendientes', 'Vencidas'],
    colors: [c.success, c.warning, c.error, '#B71C1C'],
    legend: { position: 'bottom', labels: { colors: c['on-surface'] } },
    dataLabels: { enabled: false },
    stroke: { show: false },
    theme: { mode: theme.global.name.value },
    plotOptions: { pie: { donut: { size: '68%' } } }
  }
})

/* ==========================================
   TAREAS CRÍTICAS Y COLORES DE PRIORIDAD
========================================== */
const tareasPendientes = computed(() => {
  return reportData.value ? reportData.value.tareas_criticas : []
})

const prioridadColor = (prioridad) => {
  switch (prioridad?.toLowerCase()) {
    case 'alta': return 'error'
    case 'media': return 'warning'
    case 'baja': return 'success'
    default: return 'grey'
  }
}

</script>

<style scoped>
/* ==========================================
   TOKENS Y BASE
========================================== */
.dashboard {
  --gap: 20px;
  --radius: 10px;
}

.dashboard__loader {
  height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* ==========================================
   HEADER
========================================== */
.dashboard__header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  margin-bottom: 28px;
}

.eyebrow {
  display: block;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: rgb(var(--v-theme-primary));
  margin-bottom: 4px;
}

.dashboard__title {
  font-size: 24px;
  font-weight: 600;
  letter-spacing: -0.01em;
  margin: 0;
}

.role-chip {
  text-transform: capitalize;
  font-weight: 500;
}

/* ==========================================
   STAT CARDS — grid uniforme, sin huecos
========================================== */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: var(--gap);
  margin-bottom: var(--gap);
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 18px 20px;
  border-radius: var(--radius);
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
  background: rgb(var(--v-theme-surface));
}

.stat-card__icon {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-card__value {
  font-size: 22px;
  font-weight: 700;
  line-height: 1.1;
  margin: 0;
}

.stat-card__label {
  font-size: 12px;
  color: rgba(var(--v-theme-on-surface), 0.6);
  margin: 2px 0 0;
}

/* ==========================================
   PANELS (gráficas / listas)
========================================== */
.section-row {
  margin-top: 4px;
}

.panel {
  height: 100%;
  padding: 22px;
  border-radius: var(--radius);
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
  background: rgb(var(--v-theme-surface));
}

.panel__header {
  margin-bottom: 18px;
}

.panel__title {
  font-size: 15px;
  font-weight: 600;
  margin: 0;
}

.panel__subtitle {
  font-size: 12.5px;
  color: rgba(var(--v-theme-on-surface), 0.55);
}

.empty-state {
  padding: 56px 0;
  text-align: center;
  font-size: 13.5px;
  color: rgba(var(--v-theme-on-surface), 0.5);
}

.empty-state--success {
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* ==========================================
   TASK LIST
========================================== */
.task-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
}

.task-item {
  position: relative;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 14px 8px 14px 16px;
  border-bottom: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
}

.task-item:last-child {
  border-bottom: none;
}

.task-item__priority-bar {
  position: absolute;
  left: 0;
  top: 10px;
  bottom: 10px;
  width: 3px;
  border-radius: 2px;
}

.bar--error   { background: rgb(var(--v-theme-error)); }
.bar--warning { background: rgb(var(--v-theme-warning)); }
.bar--success { background: rgb(var(--v-theme-success)); }
.bar--grey    { background: rgba(var(--v-theme-on-surface), 0.3); }

.task-item__icon {
  margin-top: 2px;
  flex-shrink: 0;
}

.task-item__body {
  flex: 1;
  min-width: 0;
}

.task-item__title {
  font-size: 14px;
  font-weight: 600;
  margin: 0 0 2px;
}

.task-item__meta {
  font-size: 12.5px;
  color: rgba(var(--v-theme-on-surface), 0.6);
  margin: 0;
  display: flex;
  align-items: center;
  gap: 6px;
}

.task-item__project {
  color: rgb(var(--v-theme-primary));
  font-weight: 500;
}

.dot {
  opacity: 0.5;
}

@media (max-width: 600px) {
  .dashboard__header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .task-item {
    flex-wrap: wrap;
  }
}
</style>