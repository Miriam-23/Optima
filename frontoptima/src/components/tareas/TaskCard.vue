<template>
  <v-card
    class="task-card pa-3"
    elevation="3"
    rounded="lg"
    draggable="true"
    @dragstart="$emit('drag-start', task)"

  >
    <!-- CABECERA -->
    <div class="d-flex justify-space-between align-center mb-3">

      <v-chip :color="priority.color" size="small" class="priority-pill">
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
            @click="$emit('delete', task)"
          />

        </v-list>
      </v-menu>

    </div>

    <!-- TITULO -->
    <div class="task-title">
      {{ task.titulo }}
    </div>

    <!-- FOOTER COMPACTO -->
    <div class="card-footer d-flex justify-space-between align-center mt-4">

      <div class="footer-left d-flex align-center">
        <div class="d-flex align-center mr-4">
          <v-icon size="16">mdi-calendar-outline</v-icon>
          <span class="text-caption ml-1">{{ task.fecha_limite || '-' }}</span>
        </div>

        <div class="d-flex align-center">
          <v-icon size="16">mdi-comment-outline</v-icon>
          <span class="text-caption ml-1">{{ task.total_comentarios ?? 0 }}</span>
        </div>
      </div>

      <div class="footer-right d-flex align-center">
        <v-avatar size="28" class="ml-2">
          <template v-if="hasAvatar">
            <img :src="responsableImagen" alt="avatar" />
          </template>
          <template v-else>
            <span class="avatar-initials">{{ initials }}</span>
          </template>
        </v-avatar>
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
  'drag-start',
  'comment-added'
])

const priority = computed(() => {
  switch (props.task.prioridad) {
    case 'Alta': return { color: 'error', text: 'Alta'}
    case 'Media': return { color: 'warning', text: 'Media'}
    default: return { color: 'success', text: 'Baja'}
  }
})

const responsable = computed(() => props.task.responsables?.[0] ?? null)

const initials = computed(() => {
  const nombre = responsable.value?.nombre || ''
  if (!nombre) return ''
  const parts = nombre.trim().split(/\s+/)
  const first = parts[0]?.charAt(0) || ''
  const second = parts[1]?.charAt(0) || ''
  return (first + second).toUpperCase()
})

const hasAvatar = computed(() => Boolean(responsable.value?.imagen || responsable.value?.avatar || responsable.value?.foto))

const responsableImagen = computed(() => responsable.value?.imagen || responsable.value?.avatar || responsable.value?.foto || '')

</script>

<style scoped>

.task-card{
  cursor:pointer;
  transition: transform .18s ease, box-shadow .18s ease;
  border-radius: 10px;
  padding: 12px;
  box-shadow: 0 6px 18px rgba(var(--v-theme-on-surface), 0.04);
  border-left: 4px solid rgba(var(--v-theme-primary), 0.12);
  background: rgb(var(--v-theme-surface));
  color: rgba(var(--v-theme-on-surface), 1);
}

.task-card:hover{
  transform: scale(1.02);
  box-shadow: 0 18px 36px rgba(var(--v-theme-on-surface), 0.08);
}

.task-title{
  font-size:1.05rem;
  font-weight:700;
  display:-webkit-box;
  -webkit-line-clamp:2;
  -webkit-box-orient:vertical;
  overflow:hidden;
  word-break: normal;
}

.priority-pill{
  border-radius: 999px;
  color: white;
  padding: 0 8px;
  text-transform: uppercase;
  font-weight: 600;
}

.card-footer{
  width:100%;
  align-items:center;
}

.footer-left .text-caption{
  color: rgba(var(--v-theme-on-surface), 0.64);
}

.avatar-initials{
  display:inline-flex;
  width:100%;
  height:100%;
  align-items:center;
  justify-content:center;
  font-weight:600;
  color: rgb(var(--v-theme-on-primary));
  background: rgb(var(--v-theme-primary));
  border-radius: 50%;
  display:block;
  line-height:28px;
}

</style>