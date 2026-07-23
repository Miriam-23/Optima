<template>
  <!-- ENCABEZADO PARA FILTRAR -->
  <TaskFilters @new-task="nuevaTarea" @update:filters="setFilters" />

  <!-- KANBAN -->
  <TaskBoard 
    :pendiente="pendiente"
    :progreso="progreso"
    :revision="revision"
    :completado="completado"
    @open="abrirDetalle"
    @edit="editar" 
    @delete="confirmarEliminar"
  />

  <!-- DIALOGO PARA EDITAR UNA TAREA -->
  <TaskDialog v-model="dialog" :task="selectedTask" @save="guardarTarea" />

  <!-- VISUALIZAR DE LA TAREA SUS DETALLES -->
  <TaskDetailDialog v-model="dialogDetalle" :task="tareaSeleccionada" />

</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useTareasStore } from '@/stores/tareas'
import TaskDialog from '@/components/tareas/TaskDialog.vue'
import TaskBoard from '@/components/tareas/TaskBoard.vue'
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

const abrirDetalle = (task)=>{
  tareaSeleccionada.value = task
  dialogDetalle.value = true
}

const {
  pendiente,
  progreso,
  revision,
  completado
} = storeToRefs(store)

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
        timer: 1500,
        showConfirmButton: false
      })

    } else {

      const tarea = await store.crearTarea(data)
      console.log("TAREA CREADA:", tarea)

      if (data.responsable) {
        console.log("Asignando usuario:", data.responsable)
        const res = await assignmentService.crearAsignacion({
          tarea: tarea.id,
          usuario: data.responsable
        })
        console.log("RESPUESTA ASIGNACIÓN:", res.data)
      }

      // Linea añadida para actualizar los filtros después de crear una tarea
      await store.setFilters(store.filters)

      await Swal.fire({
        icon: 'success',
        title: 'Tarea creada',
        text: 'La tarea se creó correctamente.',
        timer: 1500,
        showConfirmButton: false
      })

    }

    dialog.value = false
    selectedTask.value = null

  } catch (error) {

    console.error(error)

    console.log("STATUS:", error.response?.status)
    console.log("BODY:", error.response?.data)

    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'No se pudo guardar la tarea.',
      showConfirmButton: false
    })

  }

}

const confirmarEliminar = async (task) => {

  const result = await Swal.fire({
    title: '¿Eliminar tarea?',
    text: task.titulo,
    icon: 'warning',
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
      showConfirmButton: false
    })

  } catch (error) {

    Swal.fire({
      icon: 'error',
      title: 'No se pudo eliminar',
      text: error.response?.data?.detail || 'Error del servidor'
    })

  }

}

onMounted(async () => {
  const initialFilters = {}

  if (route.query.proyecto) {
    initialFilters.proyecto = Number(route.query.proyecto)
  }

  await store.setFilters(initialFilters)
})
</script>