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
import { useTasks } from '@/composables/useTask'


defineEmits([
    'open',
    'edit',
    'delete'
])

const {
    pendiente,
    progreso,
    revision,
    completado
} = useTasks()

const columns = computed(() => [
    {
        title: 'Por hacer',
        icon: 'mdi-clipboard-outline',
        color: 'grey',
        tasks: pendiente.value
    },
    {
        title: 'En progreso',
        icon: 'mdi-progress-clock',
        color: 'orange',
        tasks: progreso.value
    },
    {
        title: 'En revisión',
        icon: 'mdi-eye-check',
        color: 'blue',
        tasks: revision.value
    },
    {
        title: 'Terminadas',
        icon: 'mdi-check-circle',
        color: 'green',
        tasks: completado.value
    }
])

</script>