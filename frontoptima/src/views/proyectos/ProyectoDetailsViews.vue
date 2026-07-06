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

      <!-- 📌 FILA 1: KPIs (100% del ancho para respirar) -->
      <v-row class="mb-4">
        <v-col cols="12">
          <ProyectoKPIs :project-id="projectId" :dashboard-data="projectDashboard" />  
        </v-col>
      </v-row>

      <!-- 📌 FILA 2: TAREAS Y EQUIPO (Alineados a la misma altura) -->
      <v-row class="mb-4 align-stretch">
        <!-- Tareas (Izquierda, ligeramente más ancha para leer bien las descripciones) -->
        <v-col cols="12" lg="7" md="6" class="d-flex flex-column">
          <ProyectoUltimasTareas 
            :project-id="projectId" 
            :tareas-data="projectDashboard.tareas" 
            class="flex-grow-1" 
          />
        </v-col>

        <!-- Equipo (Derecha) -->
        <v-col cols="12" lg="5" md="6" class="d-flex flex-column">
          <EquipoProyecto 
            :project-id="projectId" 
            :equipo-data="projectDashboard.carga_por_miembro" 
            @refresh="fetchDashboard"
            class="flex-grow-1"
          /> 
        </v-col>
      </v-row>

      <!-- 📌 FILA 3: GRÁFICAS -->
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

        <!-- GRÁFICA DE BARRAS: Carga por Miembro -->
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

    </div>
  </v-container>
</template>

<script setup>
// Unificamos todas las importaciones en la parte superior para un código más limpio
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

// Convertimos el ID a número desde el principio para evitar el Warning en consola
const projectId = Number(route.params.id)

// Variables reactivas
const projectDashboard = ref(null)
const loading = ref(false)
const error = ref(null)
const dialog = ref(false)

// Llamada a la API Maestra
const fetchDashboard = async () => {
  loading.value = true
  error.value = null

  try {
    const res = await projectService.getDashboard(projectId)
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

// --- CONFIGURACIÓN DONA (Distribución) ---
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
    legend: { position: 'bottom' } // Mejor distribución en pantallas pequeñas
  }
})

// --- CONFIGURACIÓN BARRAS (Rendimiento por miembro) ---
const barSeries = computed(() => {
  if (!projectDashboard.value?.carga_por_miembro) return []
  return [
    {
      name: 'Total Tareas',
      data: projectDashboard.value.carga_por_miembro.map(m => m.total_tareas)
    },
    {
      name: 'Vencidas',
      data: projectDashboard.value.carga_por_miembro.map(m => m.tareas_vencidas)
    }
  ]
})

const barOptions = computed(() => {
  if (!projectDashboard.value?.carga_por_miembro) return {}
  return {
    chart: { toolbar: { show: false } },
    plotOptions: { bar: { borderRadius: 4, horizontal: false } },
    xaxis: { categories: projectDashboard.value.carga_por_miembro.map(m => m.nombre) },
    colors: [theme.current.value.colors.primary, theme.current.value.colors.error],
    dataLabels: { enabled: false }
  }
})
</script>