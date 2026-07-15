<template>
  <v-card class="pa-4 mb-4" elevation="2">

    <!-- HEADER -->
    <v-row align="center">

      <v-col cols="12" md="8">

        <h2 class="mb-1">
          {{ project.nombre }}
        </h2>

        <p class="text-medium-emphasis">
          {{ project.descripcion || 'Sin descripción' }}
        </p>

      </v-col>

      <v-col cols="12" md="4" class="text-md-right">

        <v-chip
          :color="estadoColor(project.estado_general)"
          variant="flat"
        >
          {{ project.estado_general }}
        </v-chip>

      </v-col>

    </v-row>

    <v-divider class="my-3" />

    <!-- FECHAS -->
    <v-row>

      <v-col cols="12" md="6">
        <strong>Fecha inicio</strong>
        <div>{{ project.fecha_inicio }}</div>
      </v-col>

      <v-col cols="12" md="6">
        <strong>Fecha fin</strong>
        <div>{{ project.fecha_fin || 'No definida' }}</div>
      </v-col>

    </v-row>

  </v-card>
</template>

<script setup>
defineProps({
  project: {
    type: Object,
    required: true
  }
})

const estadoColor = (estado) => {
  switch (estado) {
    case 'En progreso': return 'orange'
    case 'Completado': return 'green'
    case 'Pausado': return 'red'
    case 'Planificacion': return 'blue'
    default:
      return 'grey'
  }
}
</script>