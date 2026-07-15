<template>
  <v-card class="pa-4 mb-4" elevation="2">

    <!-- HEADER -->
    <div class="d-flex justify-space-between align-center mb-3">
      <h3>Últimas tareas</h3>
      <!-- Aquí podrías poner un router-link hacia la vista completa de tareas después -->
      <v-btn size="small" variant="text" color="primary" @click="verTareas">
        Ver todas
      </v-btn>
    </div>

    <!-- LISTA -->
    <v-list v-if="tareas.length">
      <v-list-item v-for="t in tareas" :key="t.id">

        <!-- ICONO SEGÚN ESTADO -->
        <template #prepend>
          <v-icon :color="estadoColor(t.estado)">
            {{ estadoIcon(t.estado) }}
          </v-icon>
        </template>

        <!-- TITULO -->
        <v-list-item-title class="font-weight-bold">
          {{ t.titulo }}
        </v-list-item-title>

        <!-- SUBTITULO -->
        <v-list-item-subtitle>
          {{ t.descripcion || 'Sin descripción' }}
        </v-list-item-subtitle>

        <!-- ESTADO -->
        <template #append>
          <v-chip size="small" :color="estadoColor(t.estado)" class="text-capitalize">
            {{ t.estado }}
          </v-chip>
        </template>

      </v-list-item>
    </v-list>

    <!-- EMPTY STATE -->
    <v-alert v-else type="info" class="mt-3" variant="tonal">
      No hay tareas registradas en este proyecto.
    </v-alert>

  </v-card>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const props = defineProps({
  projectId: {
    type: [Number, String],
    required: true
  },
  // 1. Recibimos la lista real desde tu API
  tareasData: {
    type: Array,
    default: () => []
  }
})

const verTareas = () => {

  router.push({
    name: 'tareas',
    query: {
      proyecto: props.projectId
    }
  })

}

// 2. Mapeamos las tareas. Usamos slice(0, 5) por si Django te manda 50, 
// no romper el diseño de esta tarjeta resumen.
const tareas = computed(() => {
  return (props.tareasData || []).slice(0, 5)
})

/* ICONOS (A prueba de balas: Inglés o Español) */
const estadoIcon = (estado) => {
  const e = estado ? estado.toString().toLowerCase() : ''
  if (e.includes('done') || e.includes('completado')) return 'mdi-check-circle'
  if (e.includes('doing') || e.includes('progreso')) return 'mdi-progress-clock'
  if (e.includes('todo') || e.includes('pendiente')) return 'mdi-circle-outline'
  return 'mdi-help-circle'
}

/* COLORES (A prueba de balas: Inglés o Español) */
const estadoColor = (estado) => {
  const e = estado ? estado.toString().toLowerCase() : ''
  if (e.includes('done') || e.includes('completado')) return 'success' // Usamos variables de Vuetify
  if (e.includes('doing') || e.includes('progreso')) return 'warning'
  if (e.includes('todo') || e.includes('pendiente')) return 'error'
  return 'grey'
}
</script>