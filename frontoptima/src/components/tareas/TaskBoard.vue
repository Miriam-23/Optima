<template>
    <v-row>

        <v-col
            cols="12"
            md="3"
            v-for="column in columns"
            :key="column.status"
        >

            <TaskColumn
                :title="column.title"
                :icon="column.icon"
                :color="column.color"
                :tasks="column.tasks"

                @open="$emit('open',$event)"
                @edit="$emit('edit',$event)"
                @delete="$emit('delete',$event)"
            />

        </v-col>

    </v-row>
</template>

<script setup>
import { computed } from 'vue'
import TaskColumn from '@/components/tareas/TaskColumn.vue'

defineEmits([
    'open',
    'edit',
    'delete'
])

const props = defineProps({
  pendiente: {
    type: Array,
    default: () => []
  },
  progreso: {
    type: Array,
    default: () => []
  },
  revision: {
    type: Array,
    default: () => []
  },
  completado: {
    type: Array,
    default: () => []
  }
})

const columns = computed(() => [
    {
        title: 'Por hacer',
        icon: 'mdi-clipboard-outline',
        color: 'red',
        tasks: props.pendiente
    },
    {
        title: 'En progreso',
        icon: 'mdi-progress-clock',
        color: 'orange',
        tasks: props.progreso
    },
    {
        title: 'En revisión',
        icon: 'mdi-eye-check',
        color: 'blue',
        tasks: props.revision
    },
    {
        title: 'Terminadas',
        icon: 'mdi-check-circle',
        color: 'green',
        tasks: props.completado
    }
])

</script>