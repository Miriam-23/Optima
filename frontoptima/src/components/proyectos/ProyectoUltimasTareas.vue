<template>
  <v-card class="pa-4 mb-4" elevation="2">

    <!-- HEADER -->
    <div class="d-flex justify-space-between align-center mb-3">

      <h3>Últimas tareas</h3>

      <v-btn
        size="small"
        variant="text"
        color="primary"
      >
        Ver todas
      </v-btn>

    </div>

    <!-- LISTA -->
    <v-list v-if="tareas.length">

      <v-list-item
        v-for="t in tareas"
        :key="t.id"
      >

        <!-- ICONO SEGÚN ESTADO -->
        <template #prepend>
          <v-icon :color="estadoColor(t.estado)">
            {{ estadoIcon(t.estado) }}
          </v-icon>
        </template>

        <!-- TITULO -->
        <v-list-item-title>
          {{ t.titulo }}
        </v-list-item-title>

        <!-- SUBTITULO -->
        <v-list-item-subtitle>
          {{ t.descripcion }}
        </v-list-item-subtitle>

        <!-- ESTADO -->
        <template #append>
          <v-chip
            size="small"
            :color="estadoColor(t.estado)"
          >
            {{ t.estado }}
          </v-chip>
        </template>

      </v-list-item>

    </v-list>

    <!-- EMPTY -->
    <v-alert
      v-else
      type="info"
      class="mt-3"
    >
      No hay tareas registradas
    </v-alert>

  </v-card>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  projectId: {
    type: Number,
    required: true
  }
})

/**
 * 🔥 MOCK temporal
 * Luego conectaremos a:
 * GET /api/tasks/?project=ID
 */
const tareas = computed(() => [
  {
    id: 1,
    titulo: 'Login del sistema',
    descripcion: 'Crear autenticación con JWT',
    estado: 'done'
  },
  {
    id: 2,
    titulo: 'Dashboard',
    descripcion: 'Diseñar KPIs principales',
    estado: 'doing'
  },
  {
    id: 3,
    titulo: 'API Usuarios',
    descripcion: 'Conectar backend usuarios',
    estado: 'todo'
  }
])

/* ICONOS */
const estadoIcon = (estado) => {
  switch (estado) {
    case 'done':
      return 'mdi-check-circle'
    case 'doing':
      return 'mdi-progress-clock'
    case 'todo':
      return 'mdi-circle-outline'
    default:
      return 'mdi-help-circle'
  }
}

/* COLORES */
const estadoColor = (estado) => {
  switch (estado) {
    case 'done':
      return 'green'
    case 'doing':
      return 'orange'
    case 'todo':
      return 'red'
    default:
      return 'grey'
  }
}
</script>