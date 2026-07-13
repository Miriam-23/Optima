<template>
  <v-container fluid class="pa-4 bg-background">

    <!-- LOADING -->
    <v-progress-linear v-if="loading" indeterminate color="primary" class="mb-4" />

    <!-- ERROR -->
    <v-alert v-if="error" type="error" class="mb-4" variant="tonal">
      {{ error }}
    </v-alert>

    <!-- CONTENIDO -->
    <div v-if="projectDashboard">

      <!-- HEADER -->
      <v-row class="mb-4" align="center">
        <v-col cols="12">
          <h2 class="text-h4 font-weight-bold text-primary">{{ projectDashboard.nombre || 'Dashboard del Proyecto' }}</h2>
        </v-col>
      </v-row>

      <!-- INFO DEL PROYECTO -->
      <v-row class="mb-4">
        <v-col cols="12">
          <ProyectoInfoCard :project="projectDashboard" />
        </v-col>
      </v-row>

      <!-- FILA 1: KPIs -->
      <v-row class="mb-4">
        <v-col cols="12">
          <ProyectoKPIs :project-id="projectId" :dashboard-data="projectDashboard" />
        </v-col>
      </v-row>

      <!-- FILA 2: TAREAS Y EQUIPO -->
      <v-row class="mb-4 align-stretch">
        <v-col cols="12" lg="7" md="6" class="d-flex flex-column">
          <ProyectoUltimasTareas
            :project-id="projectId"
            :tareas-data="projectDashboard.tareas"
            class="flex-grow-1"
          />
        </v-col>

        <v-col cols="12" lg="5" md="6" class="d-flex flex-column">
          <EquipoProyecto
            :project-id="projectId"
            :equipo-data="projectDashboard.carga_por_miembro"
            @refresh="fetchDashboard"
            class="flex-grow-1"
          />
        </v-col>
      </v-row>

      <!-- FILA 3: GRÁFICAS PRINCIPALES -->
      <v-row class="mb-4 align-stretch">
        <!-- GRÁFICA DE DONA: Distribución por estado -->
        <v-col cols="12" lg="4" md="5" class="d-flex flex-column">
          <v-card class="pa-4 flex-grow-1 d-flex flex-column" elevation="2">
            <h3 class="mb-4 text-subtitle-1 font-weight-bold">Distribución de Tareas</h3>
            <div class="flex-grow-1 d-flex align-center justify-center">
              <apexchart
                v-if="projectDashboard.distribucion_por_estado.length > 0"
                type="donut"
                width="100%"
                height="300"
                :options="donutOptions"
                :series="donutSeries"
              />
              <v-alert v-else type="info" variant="tonal" class="w-100">Sin datos de distribución</v-alert>
            </div>
          </v-card>
        </v-col>

        <!-- GRÁFICA DE BARRAS: Tareas por Miembro (total vs vencidas) -->
        <v-col cols="12" lg="8" md="7" class="d-flex flex-column">
          <v-card class="pa-4 flex-grow-1 d-flex flex-column" elevation="2">
            <h3 class="mb-4 text-subtitle-1 font-weight-bold">Rendimiento por Miembro</h3>
            <div class="flex-grow-1 d-flex align-center justify-center">
              <apexchart
                v-if="projectDashboard.carga_por_miembro.length > 0"
                type="bar"
                width="100%"
                height="300"
                :options="barOptions"
                :series="barSeries"
              />
              <v-alert v-else type="info" variant="tonal" class="w-100">Sin miembros asignados</v-alert>
            </div>
          </v-card>
        </v-col>
      </v-row>

      <!-- FILA 4: ESFUERZO ESTIMADO Y ALERTAS (gráficas separadas, sin mezclar escalas) -->
      <v-row class="align-stretch">
        <!-- GRÁFICA DE BARRAS HORIZONTALES: Esfuerzo estimado por miembro -->
        <v-col cols="12" lg="7" md="6" class="d-flex flex-column">
          <v-card class="pa-4 flex-grow-1 d-flex flex-column" elevation="2">
            <h3 class="mb-1 text-subtitle-1 font-weight-bold">Esfuerzo Estimado por Miembro</h3>
            <span class="text-caption text-medium-emphasis mb-4">Horas totales asignadas por persona</span>
            <div class="flex-grow-1 d-flex align-center justify-center">
              <apexchart
                v-if="projectDashboard.carga_por_miembro.length > 0"
                type="bar"
                width="100%"
                height="280"
                :options="effortOptions"
                :series="effortSeries"
              />
              <v-alert v-else type="info" variant="tonal" class="w-100">Sin datos de esfuerzo</v-alert>
            </div>
          </v-card>
        </v-col>

        <!-- GRÁFICA RADIAL: Salud del proyecto (avance + alertas) -->
        <v-col cols="12" lg="5" md="6" class="d-flex flex-column">
          <v-card class="pa-4 flex-grow-1 d-flex flex-column" elevation="2">
            <h3 class="mb-1 text-subtitle-1 font-weight-bold">Salud del Proyecto</h3>
            <span class="text-caption text-medium-emphasis mb-4">Avance general y tareas en riesgo</span>
            <div class="flex-grow-1 d-flex align-center justify-center">
              <apexchart
                type="radialBar"
                width="100%"
                height="280"
                :options="healthOptions"
                :series="healthSeries"
              />
            </div>
          </v-card>
        </v-col>
      </v-row>

    </div>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useTheme } from 'vuetify'
import projectService from '@/services/project.service'

import ProyectoInfoCard from '@/components/proyectos/ProyectoInfoCard.vue'
import ProyectoKPIs from '@/components/proyectos/ProyectoKPIs.vue'
import EquipoProyecto from '@/components/proyectos/EquipoProyecto.vue'
import ProyectoUltimasTareas from '@/components/proyectos/ProyectoUltimasTareas.vue'

const route = useRoute()
const theme = useTheme()

const projectId = Number(route.params.id)

const projectDashboard = ref(null)
const loading = ref(false)
const error = ref(null)

const fetchDashboard = async () => {
  loading.value = true
  error.value = null

  try {
    const res = await projectService.getDashboard(projectId)
    console.log(res.data)
    projectDashboard.value = res.data
  } catch (err) {
    error.value = err.response?.data?.message || 'Error al cargar las métricas del proyecto'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchDashboard()
})

/* ==========================================
   DONA: Distribución por estado
========================================== */
const donutSeries = computed(() => {
  if (!projectDashboard.value?.distribucion_por_estado) return []
  return projectDashboard.value.distribucion_por_estado.map(e => e.total)
})

const donutOptions = computed(() => {
  if (!projectDashboard.value?.distribucion_por_estado) return {}
  return {
    labels: projectDashboard.value.distribucion_por_estado.map(e => e.estado__nombre),
    theme: { mode: theme.global.name.value },
    colors: ['#FFB300', '#FF5252', '#4CAF50', '#2196F3'],
    legend: { position: 'bottom' }
  }
})

/* ==========================================
   BARRAS: Total tareas vs vencidas por miembro
========================================== */
const barSeries = computed(() => {
  if (!projectDashboard.value?.carga_por_miembro) return []
  const miembros = projectDashboard.value.carga_por_miembro
  return [
    { name: 'Total Tareas', data: miembros.map(m => m.total_tareas) },
    { name: 'Completadas', data: miembros.map(m => m.tareas_completadas) },
    { name: 'Vencidas', data: miembros.map(m => m.tareas_vencidas) }
  ]
})

const barOptions = computed(() => {
  if (!projectDashboard.value?.carga_por_miembro) return {}
  const c = theme.current.value.colors
  return {
    chart: { toolbar: { show: false } },
    plotOptions: { bar: { borderRadius: 4, horizontal: false, columnWidth: '55%' } },
    xaxis: { categories: projectDashboard.value.carga_por_miembro.map(m => m.nombre) },
    colors: [c.primary, c.success, c.error],
    dataLabels: { enabled: false },
    legend: { position: 'top' }
  }
})

/* ==========================================
   BARRAS HORIZONTALES: Esfuerzo estimado (horas) por miembro
   Gráfica separada a propósito: mezclar horas con conteos de
   tareas en el mismo eje distorsiona ambas escalas.
========================================== */
const effortSeries = computed(() => {
  if (!projectDashboard.value?.carga_por_miembro) return []
  return [{
    name: 'Horas estimadas',
    data: projectDashboard.value.carga_por_miembro.map(m => m.esfuerzo_estimado_total || 0)
  }]
})

const effortOptions = computed(() => {
  if (!projectDashboard.value?.carga_por_miembro) return {}
  const c = theme.current.value.colors
  return {
    chart: { toolbar: { show: false } },
    plotOptions: {
      bar: { horizontal: true, borderRadius: 4, barHeight: '55%', distributed: true }
    },
    xaxis: {
      categories: projectDashboard.value.carga_por_miembro.map(m => m.nombre),
      title: { text: 'Horas' }
    },
    colors: [c.primary, c.info, c.success, c.warning, c.error, c.secondary],
    dataLabels: {
      enabled: true,
      formatter: val => `${val}h`,
      style: { colors: [c['on-surface']] },
      offsetX: 8
    },
    legend: { show: false },
    tooltip: { y: { formatter: val => `${val} horas` } }
  }
})

/* ==========================================
   RADIAL: Salud del proyecto (avance general + tareas en riesgo)
   Usa 'avance.porcentaje' y 'alertas', que la API ya devuelve
   pero que hasta ahora no se visualizaban en ningún lado.
========================================== */
const healthSeries = computed(() => {
  if (!projectDashboard.value) return [0, 0]
  const total = projectDashboard.value.avance?.total_tareas || 0
  const enRiesgo = projectDashboard.value.alertas?.tareas_en_riesgo_retraso || 0
  const vencidas = projectDashboard.value.alertas?.tareas_vencidas || 0

  const porcentajeAvance = projectDashboard.value.avance?.porcentaje || 0
  // Invertimos "en riesgo + vencidas" a porcentaje para representarlo como salud, no como avance
  const porcentajeSalud = total > 0
    ? Math.max(0, 100 - Math.round(((enRiesgo + vencidas) / total) * 100))
    : 100

  return [porcentajeAvance, porcentajeSalud]
})

const healthOptions = computed(() => {
  const c = theme.current.value.colors
  return {
    chart: { toolbar: { show: false } },
    labels: ['Avance general', 'Salud (sin riesgo)'],
    colors: [c.primary, c.success],
    plotOptions: {
      radialBar: {
        hollow: { size: '40%' },
        dataLabels: {
          name: { fontSize: '12px' },
          value: { fontSize: '18px', formatter: val => `${val}%` },
          total: {
            show: true,
            label: 'Estado',
            formatter: () => {
              const vencidas = projectDashboard.value?.alertas?.tareas_vencidas || 0
              const enRiesgo = projectDashboard.value?.alertas?.tareas_en_riesgo_retraso || 0
              if (vencidas > 0) return `${vencidas} vencida(s)`
              if (enRiesgo > 0) return `${enRiesgo} en riesgo`
              return 'Al día'
            }
          }
        }
      }
    },
    legend: { show: true, position: 'bottom' }
  }
})
</script>