<template>
  <v-card class="pa-4 mb-6" rounded="lg" elevation="1">
    <v-row align="center">

      <!-- BUSCADOR -->
      <v-col cols="12" md="4">

        <v-text-field
          v-model="filters.search"
          prepend-inner-icon="mdi-magnify"
          label="Buscar tarea..."
          variant="outlined"
          density="comfortable"
          hide-details
          clearable
        />

      </v-col>

      <!-- PROYECTO -->
      <v-col cols="12" md="2">

        <v-select
          v-model="filters.proyecto"
          :items="proyectos"
          item-title="nombre"
          item-value="id"
          label="Proyecto"
          variant="outlined"
          density="comfortable"
          hide-details
          clearable
        />

      </v-col>

      <!-- ESTADO -->
      <v-col cols="12" md="2">

        <v-select
          v-model="filters.estado"
          :items="estados"
          item-title="nombre"
          item-value="id"
          label="Estado"
          variant="outlined"
          density="comfortable"
          hide-details
          clearable
        />

      </v-col>

      <!-- PRIORIDAD -->
      <v-col cols="12" md="2">

        <v-select
          v-model="filters.prioridad"
          :items="prioridades"
          label="Prioridad"
          variant="outlined"
          density="comfortable"
          hide-details
          clearable
        />

      </v-col>

      <!-- BOTONES -->
      <v-col cols="12" md="2" class="d-flex justify-end ga-2">

        <!-- LIMPIAR FILTROS -->
        <v-btn icon="mdi-filter-off" variant="text" @click="limpiar" />

        <!-- CREACION DE NUEVA TAREA (MEDIANTE EVENTO) -->
        <v-btn color="primary" prepend-icon="mdi-plus" @click="$emit('new-task')">
          Nueva
        </v-btn>

      </v-col>
    </v-row>
  </v-card>
</template>

<script setup>
import { computed, watch, reactive, onMounted } from 'vue'
import { useProyectosStore } from '@/stores/proyectos'

const emit = defineEmits([
  'update:filters',
  'new-task'
])

const proyectosStore = useProyectosStore()
const proyectos = computed(() => proyectosStore.proyectos)

onMounted(() => {
  proyectosStore.obtenerProyectos()
})

const estados=[
  { id: 2, nombre: 'Por hacer' },
  { id: 3, nombre: 'En progreso' },
  { id: 4, nombre: 'En revision' },
  { id: 1, nombre: 'Completado' }
]

const prioridades = [
  'Alta',
  'Media',
  'Baja'
]

const nuevoFiltro = () => ({
  search: '',
  proyecto: null,
  estado: null,
  prioridad: null
})

const filters = reactive(nuevoFiltro())

watch(
  filters,
  () => {
    emit('update:filters', { ...filters })
  },
  {
    deep: true
  }
)

function limpiar() {
  Object.assign(filters, nuevoFiltro())
}
</script>