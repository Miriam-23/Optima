<template>
  <v-card class="pa-4 mb-4" elevation="2">

    <h3 class="mb-4">KPIs del proyecto</h3>

    <v-row>

      <!-- TOTAL -->
      <v-col cols="12" sm="6" md="3">
        <v-card class="pa-3 text-center" variant="outlined">
          <v-icon color="primary" size="32">mdi-format-list-bulleted</v-icon>
          <h2 class="mt-2">{{ kpis.total }}</h2>
          <p class="text-medium-emphasis">Tareas</p>
        </v-card>
      </v-col>

      <!-- COMPLETADAS -->
      <v-col cols="12" sm="6" md="3">
        <v-card class="pa-3 text-center" variant="outlined">
          <v-icon color="green" size="32">mdi-check-circle</v-icon>
          <h2 class="mt-2">{{ kpis.done }}</h2>
          <p class="text-medium-emphasis">Completas</p>
        </v-card>
      </v-col>

      <!-- EN PROGRESO -->
      <v-col cols="12" sm="6" md="3">
        <v-card class="pa-3 text-center" variant="outlined">
          <v-icon color="orange" size="32">mdi-progress-clock</v-icon>
          <h2 class="mt-2">{{ kpis.doing }}</h2>
          <p class="text-medium-emphasis">En progreso</p>
        </v-card>
      </v-col>

      <!-- PENDIENTES -->
      <v-col cols="12" sm="6" md="3">
        <v-card class="pa-3 text-center" variant="outlined">
          <v-icon color="red" size="32">mdi-alert-circle</v-icon>
          <h2 class="mt-2">{{ kpis.todo }}</h2>
          <p class="text-medium-emphasis">Pendientes</p>
        </v-card>
      </v-col>

    </v-row>

  </v-card>
</template>

<script setup>
import { computed } from 'vue'

// 1. Declaramos que ahora recibimos la data real desde el componente padre
const props = defineProps({
  projectId: {
    type: [Number, String], // Aceptamos String también por si la URL lo manda como texto
    required: true
  },
  dashboardData: {
    type: Object,
    default: () => ({})
  }
})

// 2. Mapeamos los datos de la API de Django a las variables que usa el diseño visual
const kpis = computed(() => {
  const data = props.dashboardData || {}
  const avance = data.avance || {}
  const alertas = data.alertas || {}
  
  return {
    total: avance.total_tareas || 0,
    done: avance.completadas || 0,
    doing: data.distribucion_por_estado?.find(e => e.estado__nombre === 'En progreso')?.total || 0,
    todo: alertas.tareas_pendientes || 0
  }
})
</script>