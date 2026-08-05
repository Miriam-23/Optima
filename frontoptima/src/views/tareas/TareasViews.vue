<template>
  <!-- ENCABEZADO PARA FILTRAR -->
  <TaskFilters @new-task="nuevaTarea" @update:filters="setFilters" />

  <!-- VISTA: Selector Kanban / Lista -->
  <div class="view-selector mb-4 d-flex">
    <v-btn
      :variant="viewMode === 'kanban' ? 'tonal' : 'text'"
      size="small"
      class="mr-2"
      @click="viewMode = 'kanban'"
    >
      Kanban
    </v-btn>

    <v-btn
      :variant="viewMode === 'list' ? 'tonal' : 'text'"
      size="small"
      @click="viewMode = 'list'"
    >
      Lista
    </v-btn>
  </div>

  <!-- VISTAS -->
  <div v-if="viewMode === 'kanban'">
    <TaskBoard 
      :pendiente="pendiente"
      :progreso="progreso"
      :en_revision="en_revision"
      :completada="completada"
      @open="abrirDetalle"
      @edit="editar" 
      @delete="confirmarEliminar"
    />
  </div>

  <div v-else>
    <TaskListView :tasks="filteredTasks" @open="abrirDetalle" />
  </div>

  <!-- DIALOGO PARA EDITAR UNA TAREA -->
  <TaskDialog v-model="dialog" :task="selectedTask" @save="guardarTarea" />

  <!-- VISUALIZAR DE LA TAREA SUS DETALLES -->
  <TaskDetailDialog v-model="dialogDetalle" :task="tareaSeleccionada" @comment-added="refreshTask" />

</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useTareasStore } from '@/stores/tareas'
import { useTheme } from 'vuetify'
import TaskDialog from '@/components/tareas/TaskDialog.vue'
import TaskBoard from '@/components/tareas/TaskBoard.vue'
import TaskListView from '@/components/tareas/TaskListView.vue'
import TaskFilters from '@/components/tareas/TaskFilters.vue'
import TaskDetailDialog from '@/components/tareas/TaskDetailsDialog.vue'
import assignmentService from '@/services/assignment.service'
import Swal from 'sweetalert2'

const store = useTareasStore()
const route = useRoute()
const dialog = ref(false)
const dialogDetalle = ref(false)
const selectedTask = ref(null)
const tareaSeleccionada = ref(null)
const theme = useTheme()
const isDark = theme.global.current.value.dark

// FUNCION PARA ABRIR EL DETALLE DE LA TAREA
const abrirDetalle = async(task)=>{

  await store.obtenerTarea(task.id)
  tareaSeleccionada.value = store.tareaActual
  dialogDetalle.value = true

}

// De acuerdo a la BD
const {
  pendiente,
  progreso,
  en_revision,
  completada,
  filteredTasks
} = storeToRefs(store)

const viewMode = ref('kanban')

const { setFilters } = store

function nuevaTarea() {
  selectedTask.value = null
  dialog.value = true
}

// FUNCION PARA EDITAR UNA TAREA
async function editar(task) {

  await store.obtenerTarea(task.id)
  selectedTask.value = store.tareaActual
  dialog.value = true
}

const guardarTarea = async (data) => {

  try {

    if (selectedTask.value) {

      await store.actualizarTarea(selectedTask.value.id, data)

      await Swal.fire({
        icon: 'success',
        title: 'Tarea actualizada',
        text: 'La tarea se actualizó correctamente.',
        background: isDark ? "#1E1E1E" : "#FFFFFF",
        color: isDark ? "#F5F5F5" : "#1F2937",
        backdrop: isDark ? "rgba(0,0,0,.75)" : "rgba(0,0,0,.45)",
        timer: 1500,
        showConfirmButton: false
      })

    } else {

      const tarea = await store.crearTarea(data)

      if (data.responsable) {
        const res = await assignmentService.crearAsignacion({
          tarea: tarea.id,
          usuario: data.responsable
        })
      }

      // Linea añadida para actualizar los filtros después de crear una tarea
      await store.setFilters(store.filters)

      await Swal.fire({
        icon: 'success',
        title: 'Tarea creada',
        text: 'La tarea se creó correctamente.',
        background: isDark ? "#1E1E1E" : "#FFFFFF",
        color: isDark ? "#F5F5F5" : "#1F2937",
        backdrop: isDark ? "rgba(0,0,0,.75)" : "rgba(0,0,0,.45)",
        timer: 1500,
        showConfirmButton: false
      })

    }

    dialog.value = false
    selectedTask.value = null

  } catch (error) {

    console.error(error)

    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'No se pudo guardar la tarea.',
      background: isDark ? "#1E1E1E" : "#FFFFFF",
      color: isDark ? "#F5F5F5" : "#1F2937",
      backdrop: isDark ? "rgba(0,0,0,.75)" : "rgba(0,0,0,.45)",
      showConfirmButton: false
    })

  }

}

const confirmarEliminar = async (task) => {

  const result = await Swal.fire({
    title: '¿Eliminar tarea?',
    text: task.titulo,
    icon: 'warning',
    background: isDark ? "#1E1E1E" : "#FFFFFF",
    color: isDark ? "#F5F5F5" : "#1F2937",
    backdrop: isDark ? "rgba(0,0,0,.75)" : "rgba(0,0,0,.45)",
    showCancelButton: true,
    confirmButtonText: 'Eliminar',
    cancelButtonText: 'Cancelar',
    reverseButtons: true
  })

  if (!result.isConfirmed) return

  try {

    await store.eliminarTarea(task.id)

    await Swal.fire({
      icon: 'success',
      title: 'Tarea eliminada',
      timer: 1200,
      showConfirmButton: false,
      background: isDark ? "#1E1E1E" : "#FFFFFF",
      color: isDark ? "#F5F5F5" : "#1F2937",
      backdrop: isDark ? "rgba(0,0,0,.75)" : "rgba(0,0,0,.45)"
    })

  } catch (error) {

    Swal.fire({
      icon: 'error',
      title: 'No se pudo eliminar',
      text: error.response?.data?.detail || 'Error del servidor',
      background: isDark ? "#1E1E1E" : "#FFFFFF",
      color: isDark ? "#F5F5F5" : "#1F2937",
      backdrop: isDark ? "rgba(0,0,0,.75)" : "rgba(0,0,0,.45)"
    })

  }

}

const refreshTask = async () => {
  await store.obtenerTareas({
    proyecto: store.filters.proyecto,
    estado: store.filters.estado,
    prioridad: store.filters.prioridad
  })
}

onMounted(async () => {
  const initialFilters = {}

  if (route.query.proyecto) {
    initialFilters.proyecto = Number(route.query.proyecto)
  }

  await store.setFilters(initialFilters)
})
</script>