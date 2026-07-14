<template>
  <v-card
    class="pa-4 mb-6"
    rounded="lg"
    elevation="1"
  >
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
          v-model="filters.proyectoId"
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
      <v-col
        cols="12"
        md="2"
        class="d-flex justify-end ga-2"
      >

        <v-btn
          icon="mdi-filter-off"
          variant="text"
          @click="limpiar"
        />

        <v-btn
          color="primary"
          prepend-icon="mdi-plus"
          @click="$emit('new-task')"
        >
          Nueva
        </v-btn>

      </v-col>

    </v-row>
  </v-card>
</template>

<script setup>
import { reactive, watch } from 'vue'
import { useProyectosStore } from '@/stores/proyectos'

const emit = defineEmits([
  'update:filters',
  'new-task'
])

const proyectosStore = useProyectosStore()

const proyectos = proyectosStore.proyectos

const estados=[
  'Por hacer',
  'En progreso',
  'En revision',
  'Completado'
]

const prioridades = [
  'Alta',
  'Media',
  'Baja'
]

const nuevoFiltro = () => ({
  search: '',
  proyectoId: null,
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