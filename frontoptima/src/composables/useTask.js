import { computed, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useTareasStore } from '@/stores/tareas'

export function useTasks() {

    const tareasStore = useTareasStore()

    const { tareas } = storeToRefs(tareasStore)

    const filters = ref({
        search: '',
        proyectoId: null,
        estado: null,
        prioridad: null
    })

    /* ===========================
       FILTRADO
    ============================ */

    const filteredTasks = computed(() => {

        return tareas.value.filter(task => {

            if (
                filters.value.search &&
                !task.titulo
                    .toLowerCase()
                    .includes(filters.value.search.toLowerCase())
            ) {
                return false
            }

            if (
                filters.value.proyectoId &&
                task.proyectoId !== filters.value.proyectoId
            ) {
                return false
            }

            if (
                filters.value.estado &&
                task.estado !== filters.value.estado
            ) {
                return false
            }

            if (
                filters.value.prioridad &&
                task.prioridad !== filters.value.prioridad
            ) {
                return false
            }
            return true
        })
    })

    /* ===========================
       COLUMNAS
    ============================ */

    const pendiente = computed(() =>
        filteredTasks.value.filter(t => t.nombre_estado === 'Por hacer')
    )

    const progreso = computed(() =>
        filteredTasks.value.filter(t => t.nombre_estado === 'En progreso')
    )

    const revision = computed(() =>
        filteredTasks.value.filter(t => t.nombre_estado === 'En revision')
    )

    const completado = computed(() =>
        filteredTasks.value.filter(t => t.nombre_estado === 'Completado')
    )

    /* ===========================
       KPIs
    ============================ */

    const stats = computed(() => ({
        total: filteredTasks.value.length,
        pendiente: pendiente.value.length,
        progreso: progreso.value.length,
        revision: revision.value.length,
        completado: completado.value.length
    }))

    /* ===========================
       MÉTODOS
    ============================ */

    function setFilters(newFilters) {
        filters.value = {
            ...filters.value,
            ...newFilters
        }
    }

    function clearFilters() {
        filters.value = {
            search: '',
            proyectoId: null,
            estado: null,
            prioridad: null
        }
    }

    return {
        filters,
        filteredTasks,
        pendiente,
        progreso,
        revision,
        completado,
        stats,
        setFilters,
        clearFilters
    }
}