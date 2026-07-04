<template>
  <div>

    <h2 class="mb-6">Dashboard</h2>

    <!-- KPIs REALES -->
    <v-row>
      <v-col cols="12" sm="6" md="2" v-for="(item, i) in statsCards" :key="i">
        <v-card class="pa-4" elevation="2" color="surface">
          <v-icon :color="item.color" size="40">{{ item.icon }}</v-icon>
          <h3 class="mt-2">{{ item.value }}</h3>
          <p class="text-medium-emphasis">{{ item.title }}</p>
        </v-card>
      </v-col>
    </v-row>

    <!-- GRÁFICAS -->
    <v-row class="mt-6">

      <!-- PROGRESO POR PROYECTO -->
      <v-col cols="12" md="8">
        <v-card class="pa-4" elevation="2">
          <h3 class="mb-4">Progreso de proyectos</h3>

          <apexchart
            type="bar"
            height="300"
            :options="chartOptions"
            :series="series"
          />
        </v-card>
      </v-col>

      <!-- ESTADO DE TAREAS -->
      <v-col cols="12" md="4">
        <v-card class="pa-4" elevation="2">
          <h3 class="mb-4">Estado de tareas</h3>

          <apexchart
            type="donut"
            height="300"
            :options="donutOptions"
            :series="donutSeries"
          />
        </v-card>
      </v-col>

    </v-row>

    <!-- TAREAS PENDIENTES -->
    <v-row class="mt-6">

      <v-col cols="12">
        <v-card class="pa-4" elevation="2">

          <h3 class="mb-4">Tareas pendientes críticas</h3>

          <v-list lines="two">

            <v-list-item
              v-for="t in tareasPendientes"
              :key="t.id"
            >

              <template #prepend>
                <v-icon :color="prioridadColor(t.prioridad)">
                  mdi-alert-circle
                </v-icon>
              </template>

              <v-list-item-title>
                {{ t.titulo }}
              </v-list-item-title>

              <v-list-item-subtitle>
                {{ t.descripcion }}
              </v-list-item-subtitle>

              <template #append>
                <v-chip
                  :color="prioridadColor(t.prioridad)"
                  size="small"
                >
                  {{ t.prioridad }}
                </v-chip>
              </template>

            </v-list-item>

          </v-list>

        </v-card>
      </v-col>

    </v-row>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useProyectosStore } from '@/stores/proyectos'
import { useTareasStore } from '@/stores/tareas'
import { useTheme } from 'vuetify'

const theme = useTheme()

const proyectosStore = useProyectosStore()
const tareasStore = useTareasStore()

/* =========================
   KPIs REALES
========================= */

const statsCards = computed(() => [
  {
    title: 'Proyectos',
    value: proyectosStore.total,
    icon: 'mdi-folder',
    color: 'primary'
  },
  {
    title: 'Tareas',
    value: tareasStore.total,
    icon: 'mdi-format-list-checkbox',
    color: 'info'
  },
  {
    title: 'Completadas',
    value: tareasStore.done.length,
    icon: 'mdi-check-circle',
    color: 'success'
  },
  {
    title: 'En progreso',
    value: tareasStore.doing.length,
    icon: 'mdi-progress-clock',
    color: 'warning'
  },
  {
    title: 'Pendientes',
    value: tareasStore.todo.length,
    icon: 'mdi-alert-circle',
    color: 'error'
  }
])

/* =========================
   GRÁFICA BARRAS (PROYECTOS)
========================= */

const colores = computed(() => {
  const c = theme.current.value.colors

  const base = [
    c.primary,
    c.accent,
    c.secondary,
    c.success,
    c.warning,
    c.info,
    c.error
  ]

  return proyectosStore.proyectos.map((_, i) => base[i % base.length])
})

const series = computed(() => [
  {
    name: 'Progreso',
    data: proyectosStore.proyectos.map(p => progresoProyecto(p.id))
  }
])

const chartOptions = computed(() => ({
  chart: {
    toolbar: { show: false }
  },

  plotOptions: {
    bar: {
      distributed: true,
      borderRadius: 8
    }
  },

  xaxis: {
    categories: proyectosStore.proyectos.map(p => p.nombre)
  },

  yaxis: {
    min: 0,
    max: 100,
    labels: {
      formatter: value => `${value}%`
    }
  },

  dataLabels: {
    enabled: true,
    formatter: value => `${value}%`
  },

  colors: colores.value
}))

/* =========================
   DONUT (TAREAS)
========================= */

const donutSeries = computed(() => [
  tareasStore.done.length,
  tareasStore.doing.length,
  tareasStore.todo.length
])

const donutOptions = computed(() => ({
  labels: ['Completadas', 'En progreso', 'Pendientes'],
  colors: [
    theme.current.value.colors.success,
    theme.current.value.colors.warning,
    theme.current.value.colors.error
  ]
}))

/* =========================
   PROGRESO POR PROYECTO
========================= */

const progresoProyecto = (id) => {
  const tareas = tareasStore.tareas.filter(t => t.proyectoId === id)

  if (tareas.length === 0) return 0

  const hechas = tareas.filter(t => t.estado === 'done').length

  return Math.round((hechas / tareas.length) * 100)
}

/* =========================
  TAREAS PENDIENTES (CRITICAS)
========================= */

const tareasPendientes = computed(() => {
  return tareasStore.tareas
    .filter(t => t.estado === 'todo')
    .sort((a, b) => {
      const orden = { alta: 3, media: 2, baja: 1 }
      return orden[b.prioridad] - orden[a.prioridad]
    })
    .slice(0, 5) // solo top 5
})

const prioridadColor = (prioridad) => {
  switch (prioridad) {
    case 'alta': return 'error'
    case 'media': return 'warning'
    case 'baja': return 'success'
    default: return 'grey'
  }
}
</script>