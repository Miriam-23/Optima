<template>
  <!-- ENCABEZADO PARA FILTRAR -->
  <TaskFilters @new-task="nuevaTarea" @update:filters="setFilters" />

  <!-- KANBAN -->
  <TaskBoard @edit="editar" />

  <!-- DIALOGO PARA EDITAR UNA TAREA -->
  <TaskDialog v-model="dialog" :task="selectedTask" />

</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useTasks } from '@/composables/useTask'
import { useTareasStore } from '@/stores/tareas'
import TaskDialog from '@/components/tareas/TaskDialog.vue'
import TaskBoard from '@/components/tareas/TaskBoard.vue'
import TaskFilters from '@/components/tareas/TaskFilters.vue'
import Swal from 'sweetalert2'

const store = useTareasStore()


const dialog = ref(false)
const selectedTask = ref(null)

const {
    filters,
    setFilters
} = useTasks()

function nuevaTarea() {
    selectedTask.value = null
    dialog.value = true
}

function editar(task) {
    selectedTask.value = task
    dialog.value = true
}

const confirmarEliminar = async (id) => {

  const result = await Swal.fire({
    title: '¿Deseas eliminar esta tarea?',
    text: 'Esta acción no se puede deshacer.',
    icon: 'warning',
    background: 'rgba(13, 194, 211,0.6)',
    color: '#fff',
    backdrop: 'rgba(0,0,0,0.4)',
    showCancelButton: true,
    confirmButtonText: 'Eliminar',
    cancelButtonText: 'Cancelar',
    confirmButtonColor: 'success',
    cancelButtonColor: 'error',
    confirmButtonColor: '#d32f2f', // Rojo
    cancelButtonColor: '#1976D2',
    customClass: {
      popup: 'swal2-glass'
    }
  })

  if (!result.isConfirmed) return

  try {

    await store.eliminarTarea(id)

    Swal.fire({
      title: 'Tarea eliminada',
      text: 'La tarea se elimino correctamente.',
      icon: 'success',
      background: 'rgba(0,0,0,0.6)',
      color: '#fff',
      backdrop: 'rgba(0,0,0,0.4)',
      showConfirmButton: false,
      timer: 1500,
      timerProgressBar: false,
      customClass: {
        popup: 'swal2-glass'
      }
    })

  } catch (error) {

    Swal.fire({
      title: 'Error',
      text: 'No se pudo eliminar la tarea.',
      icon: 'error',
      background: 'rgba(0,0,0,0.6)',
      color: '#fff',
      backdrop: 'rgba(0,0,0,0.4)',
      showConfirmButton: false,
      timer: 1500,
      timerProgressBar: false,
      customClass: {
        popup: 'swal2-glass'
      }
    })

    console.error(error)
  }
}

onMounted(async () => {
  await store.obtenerTareas()
})
</script>