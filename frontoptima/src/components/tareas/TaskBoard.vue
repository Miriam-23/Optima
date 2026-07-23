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
                :status="column.status"
                :tasks="column.tasks"

                @open="$emit('open',$event)"
                @edit="$emit('edit',$event)"
                @delete="$emit('delete',$event)"
                @drag-start="handleDragStart"
                @drop="handleDrop"
            />

        </v-col>

    </v-row>
</template>

<script setup>
import { computed, ref } from 'vue'
import TaskColumn from '@/components/tareas/TaskColumn.vue'
import { useTareasStore } from '@/stores/tareas'

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

const store = useTareasStore()
const draggedTask = ref(null)

const statusMap = {
    'Por hacer': 2,
    'En progreso': 3,
    'En revision': 4,
    'Completado': 1
}

function handleDragStart(task) {
    draggedTask.value = task
}

async function handleDrop(status) {
    if (!draggedTask.value) return

    const nuevoEstado = statusMap[status]

    if (!nuevoEstado || nuevoEstado === draggedTask.value.estado) {
        draggedTask.value = null
        return
    }

    await store.actualizarParcial(draggedTask.value.id, { estado: nuevoEstado })
    draggedTask.value = null
}

const columns = computed(() => [
    {
        title: 'Por hacer',
        icon: 'mdi-clipboard-outline',
        color: 'red',
        status: 'Por hacer',
        tasks: props.pendiente
    },
    {
        title: 'En progreso',
        icon: 'mdi-progress-clock',
        color: 'orange',
        status: 'En progreso',
        tasks: props.progreso
    },
    {
        title: 'En revision',
        icon: 'mdi-eye-check',
        color: 'blue',
        status: 'En revision',
        tasks: props.revision
    },
    {
        title: 'Completado',
        icon: 'mdi-check-circle',
        color: 'green',
        status: 'Completado',
        tasks: props.completado
    }
])

</script>