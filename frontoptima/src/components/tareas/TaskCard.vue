<template>
  <v-card
    class="task-card"
    elevation="2"
    rounded="lg"
    @click="$emit('open', task)"
  >
    <!-- CABECERA -->
    <div class="d-flex justify-space-between align-center mb-3">

      <v-chip
        :color="priority.color"
        size="small"
        variant="flat"
      >
        {{ priority.text }}
      </v-chip>

      <v-menu>
        <template #activator="{ props }">
          <v-btn
            icon
            variant="text"
            size="small"
            v-bind="props"
            @click.stop
          >
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>

        <v-list density="compact">
          <v-list-item
            prepend-icon="mdi-pencil"
            title="Editar"
            @click="$emit('edit', task)"
          />

          <v-list-item
            prepend-icon="mdi-delete"
            title="Eliminar"
            @click="$emit('delete', task)"
          />
        </v-list>
      </v-menu>

    </div>

    <!-- TITULO -->
    <div class="text-subtitle-1 font-weight-bold mb-2">
      {{ task.titulo }}
    </div>

    <!-- DESCRIPCION -->
    <div
      class="text-body-2 text-medium-emphasis mb-4 description"
    >
      {{ task.descripcion }}
    </div>

    <!-- ETIQUETAS -->
    <div
      class="d-flex flex-wrap ga-2 mb-4"
      v-if="task.etiquetas?.length"
    >
      <v-chip
        v-for="tag in task.etiquetas"
        :key="tag"
        size="x-small"
        color="primary"
        variant="outlined"
      >
        {{ tag }}
      </v-chip>
    </div>

    <!-- FOOTER -->
    <div class="d-flex justify-space-between align-center">

      <div class="d-flex align-center ga-2">

        <v-avatar
          size="30"
          color="primary"
        >
          {{ initials }}
        </v-avatar>

        <span class="text-caption">
          {{ task.responsable }}
        </span>

      </div>

      <div class="d-flex align-center ga-3">

        <div class="d-flex align-center">
          <v-icon size="18">mdi-comment</v-icon>
          <span class="text-caption ml-1">
            {{ task.comentarios }}
          </span>
        </div>

        <div class="d-flex align-center">
          <v-icon size="18">mdi-paperclip</v-icon>
          <span class="text-caption ml-1">
            {{ task.adjuntos }}
          </span>
        </div>

        <div class="text-caption">
          {{ task.fechaLimite }}
        </div>

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

defineEmits([
  'open',
  'edit',
  'delete'
])

const priority = computed(() => {
  switch (props.task.prioridad) {
    case 'Alta': return { color: 'error', text: 'Alta'}
    case 'Media': return { color: 'warning', text: 'Media'}
    default: return { color: 'success', text: 'Baja'}
  }
})

const initials = computed(() => {

  if (!props.task.responsable) return '?'
  return props.task.responsable
    .split(' ')
    .map(i => i[0])
    .join('')
    .substring(0,2)

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

.description{
  min-height:48px;
}
</style>