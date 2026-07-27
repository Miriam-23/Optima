<template>
  <v-card
    class="task-column pa-3"
    elevation="1"
    rounded="lg"
    @dragover.prevent
    @drop="$emit('drop', status)"
  >

    <!-- Header -->
    <div class="column-header d-flex justify-space-between align-center mb-4">

      <div class="d-flex align-center">

        <v-icon :color="color" class="mr-2">
          {{ icon }}
        </v-icon>

        <span class="text-h6 column-title">
          {{ title }}
        </span>

      </div>

      <v-chip size="small" color="primary" class="count-chip">
        {{ tasks.length }}
      </v-chip>

    </div>

    <!-- Cards container (scrollable) -->
    <div class="cards-wrapper">

      <TaskCard
        v-for="task in tasks"
        :key="task.id"
        :task="task"
        class="mb-3"
        @open="$emit('open', $event)"
        @edit="$emit('edit', $event)"
        @delete="$emit('delete', $event)"
        @drag-start="$emit('drag-start', $event)"
      />

      <v-sheet
        v-if="tasks.length === 0"
        class="empty-column pa-8"
        rounded="lg"
      >
        <v-icon size="50" color="grey-lighten-1">
          mdi-clipboard-text-outline
        </v-icon>

        <div class="mt-3 text-medium-emphasis">
          No hay tareas
        </div>
      </v-sheet>

    </div>

  </v-card>
</template>

<script setup>
import TaskCard from './TaskCard.vue'

defineProps({
  title: String,
  icon: String,
  color: String,
  status: String,
  tasks: {
    type: Array,
    default: () => []
  }
})

defineEmits([
  'open',
  'edit',
  'delete',
  'drag-start',
  'drop'
])

</script>

<style scoped>

.task-column{
  background: rgb(var(--v-theme-surface));
  min-height: 75vh;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.column-header{
  flex: 0 0 auto;
  padding-bottom: 4px;
}

.cards-wrapper{
  flex: 1 1 auto;
  overflow-y: auto;
  padding-right: 6px;
}

/* Keep empty column styling */
.empty-column{
  display:flex;
  flex-direction:column;
  justify-content:center;
  align-items:center;
  border:2px dashed rgba(var(--v-theme-on-surface), 0.12);
  background: transparent;
  min-height:250px;
  width:100%;
}

</style>