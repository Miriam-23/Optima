<template>
  <v-card
    class="task-card pa-2"
    elevation="3"
    rounded="small"
    draggable="true"
    @click="$emit('open', task)"
    @dragstart="$emit('drag-start', task)"
  >
    <!-- CABECERA -->
    <div class="d-flex justify-space-between align-center mb-3">

      <v-chip :color="priority.color" size="small" variant="tonal">
        {{ priority.text }}
      </v-chip>

      <v-menu>
        <template #activator="{ props }">
          <v-btn icon variant="text" size="small" v-bind="props" @click.stop>
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>

        <v-list density="compact">

          <v-list-item
            prepend-icon="mdi-eye"
            title="Ver Tarea"
            @click="$emit('open', task)"
          />

          <v-list-item
            prepend-icon="mdi-pencil"
            title="Editar"
            @click="$emit('edit', task)"
          />

          <v-list-item
            prepend-icon="mdi-delete"
            title="Eliminar"
            @click="$emit('delete', props.task)"
          />

        </v-list>
      </v-menu>

    </div>

    <!-- TITULO -->
    <div class="task-title">
      {{ task.titulo }}
    </div>

    <!-- FOOTER -->
    <div class="d-flex justify-space-between align-center mt-4">

      <!-- Información -->
      <v-row class="flex-grow-1" no-gutters>
        <v-col cols="6">
          <div class="text-caption text-medium-emphasis">
            Responsable
          </div>

          <div class="text-body-2 font-weight-medium">
            {{ task.responsables?.[0]?.nombre ?? 'Sin asignar' }}
          </div>
        </v-col>

        <v-col cols="6">
          <div class="text-caption text-medium-emphasis">
            Fecha límite
          </div>

          <div class="text-body-2">
            {{ task.fecha_limite }}
          </div>
        </v-col>
      </v-row>

      <!-- Iconos -->
      <div class="d-flex align-center ga-4 ml-4">
        <div class="d-flex align-center">
          <v-icon size="18">mdi-comment-outline</v-icon>

          <span class="text-caption ml-1">
            {{ task.total_comentarios ?? 0 }}
          </span>
        </div>

        <!-- ADJUNTAR ARCHIVOS (POR IMPLEMENTAR / MEJORA) -->
        <!-- <div class="d-flex align-center">
          <v-icon size="18">mdi-paperclip</v-icon>

          <span class="text-caption ml-1">
            {{ task.adjuntos ?? 0 }}
          </span>
        </div> -->
      </div>

    </div>
  </v-card>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  task: {
    type: Object,
    required: true
  }
})

const emit = defineEmits([
  'open',
  'edit',
  'delete',
  'drag-start'
])

const priority = computed(() => {
  switch (props.task.prioridad) {
    case 'Alta': return { color: 'error', text: 'Alta'}
    case 'Media': return { color: 'warning', text: 'Media'}
    default: return { color: 'success', text: 'Baja'}
  }
})

</script>

<style scoped>

.task-card{
  cursor:pointer;
  transition:.25s;
  border-left:5px solid rgb(var(--v-theme-primary));
}

.task-card:hover{
  transform:translateY(-4px);
  box-shadow:0 12px 30px rgba(0,0,0,.12);
}

.task-title{
  font-size:1.15rem;
  font-weight:700;
  display:-webkit-box;
  -webkit-line-clamp:2;
  -webkit-box-orient:vertical;
  overflow:hidden;
}

.description{
  color:#64748B;
  display:-webkit-box;
  -webkit-line-clamp:3;
  -webkit-box-orient:vertical;
  overflow:hidden;
  min-height:64px;
}
</style>