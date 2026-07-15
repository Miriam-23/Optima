<template>
  <!-- ENCABEZADO PARA FILTRAR -->
  <TaskFilters @new-task="nuevaTarea" @update:filters="setFilters" />

  <!-- KANBAN -->
  <TaskBoard 
    :pendiente="pendiente"
    :progreso="progreso"
    :revision="revision"
    :completado="completado"
    @edit="editar" 
    @delete="confirmarEliminar"
  />

  <!-- DIALOGO PARA EDITAR UNA TAREA -->
  <TaskDialog v-model="dialog" :task="selectedTask" @save="guardarTarea" />

</template>

<script setup>
import { ref, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useTareasStore } from '@/stores/tareas'
import TaskDialog from '@/components/tareas/TaskDialog.vue'
import TaskBoard from '@/components/tareas/TaskBoard.vue'
import TaskFilters from '@/components/tareas/TaskFilters.vue'
import Swal from 'sweetalert2'

const store = useTareasStore()

const dialog = ref(false)
const selectedTask = ref(null)

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

function editar(task) {
  selectedTask.value = task
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

      await store.crearTarea(data)

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
  await store.obtenerTareas()
})
</script>