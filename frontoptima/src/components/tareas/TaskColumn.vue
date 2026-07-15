<template>
  <v-card class="task-column pa-3" elevation="1" rounded="lg"  >

    <!-- Header -->
    <div class="d-flex justify-space-between align-center mb-4">

      <div class="d-flex align-center">

        <v-icon :color="color" class="mr-2">
          {{ icon }}
        </v-icon>

        <span class="text-h6">
          {{ title }}
        </span>

      </div>

      <v-chip size="small" color="primary">
        {{ tasks.length }}
      </v-chip>

    </div>

    <!-- Cards -->

    <TaskCard
      v-for="task in tasks"
      :key="task.id"
      :task="task"
      class="mb-3"
      @open="$emit('open', $event)"
      @edit="$emit('edit', $event)"
      @delete="$emit('delete', $event)"
    />

    <!-- Sin tareas -->

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
  </v-card>
</template>

<script setup>
import TaskCard from './TaskCard.vue'

defineProps({
  title: String,
  icon: String,
  color: String,
  tasks: {
    type: Array,
    default: () => []
  }
})

defineEmits([
  'open',
  'edit',
  'delete'
])

</script>

<style scoped>

.task-column{
  background: 'surface';
  min-height:650px;
}

.empty-column{
  display:flex;
  flex-direction:column;
  justify-content:center;
  align-items:center;
  border:2px dashed #CBD5E1;
  background:'surface';
  min-height:250px;
}

</style>