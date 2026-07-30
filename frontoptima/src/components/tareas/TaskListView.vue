<template>
  <v-card class="task-list-view pa-3" elevation="1" rounded="lg">

    <v-list density="compact">
      <v-list-item
        v-for="task in tasks"
        :key="task.id"
        class="task-list-item"
        @click="$emit('open', task)"
      >

        <v-list-item-content>
          <div class="d-flex justify-space-between align-center">
            <div>
              <div class="text-subtitle-1 font-weight-medium">{{ task.titulo }}</div>
              <div class="text-caption text-medium-emphasis">{{ task.proyecto_nombre || '' }}</div>
            </div>

            <div class="d-flex align-center">
              <v-chip :color="priorityColor(task.prioridad)" size="small" class="mr-3" text-color="white">
                {{ task.prioridad || 'Baja' }}
              </v-chip>

              <div class="text-caption mr-4">{{ task.estado_nombre || task.nombre_estado || task.estado }}</div>

              <div class="d-flex align-center mr-3">
                <v-icon size="16">mdi-calendar-outline</v-icon>
                <span class="text-caption ml-1">{{ task.fecha_limite || '-' }}</span>
              </div>

              <v-avatar size="28">
                <template v-if="task.responsables?.[0]?.imagen">
                  <img :src="task.responsables[0].imagen" alt="avatar" />
                </template>
                <template v-else>
                  <span class="avatar-initials">{{ initials(task.responsables?.[0]?.nombre) }}</span>
                </template>
              </v-avatar>
            </div>
          </div>
        </v-list-item-content>

      </v-list-item>
    </v-list>

  </v-card>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  tasks: {
    type: Array,
    default: () => []
  }
})

function initials(name){
  if(!name) return ''
  const parts = name.trim().split(/\s+/)
  return ((parts[0]?.charAt(0) || '') + (parts[1]?.charAt(0) || '')).toUpperCase()
}

function priorityColor(p){
  switch(p){
    case 'Alta': return 'error'
    case 'Media': return 'warning'
    default: return 'success'
  }
}

</script>

<style scoped>
.task-list-view{
  background: rgb(var(--v-theme-surface));
}
.task-list-item{
  cursor: pointer;
  padding: 12px 8px;
  border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.06);
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
  line-height:28px;
}

</style>
