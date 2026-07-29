import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import taskService from '@/services/task.service'

export const useTareasStore = defineStore('tareas', () => {

  const tareas = ref([])
  const tareaActual = ref(null)
  const filters = ref({
    search:'',
    proyecto:null,
    estado:null,
    prioridad:null
  })
  
  // De acuerdo a la BD, los estados son:
  function normalizarEstado(task) {
      return task.nombre_estado || ''
  }
  // FILTRADOS
  const filteredTasks = computed(() => {

    return tareas.value.filter(task=>{

      if(
        filters.value.search &&
        !task.titulo.toLowerCase().includes(
          filters.value.search.toLowerCase()
        )
      ){
        return false
      }

      if(
        filters.value.estado &&
        Number(task.estado) !== Number(filters.value.estado)
      ){
        return false
      }

      if(
        filters.value.prioridad &&
        task.prioridad!==filters.value.prioridad
      ){
        return false
      }

      return true
    })

  })

  // COLUMNAS DE FILTROS
  const pendiente = computed(() =>
      filteredTasks.value.filter(
          t => normalizarEstado(t) === "Pendiente"
      )
  )

  const progreso = computed(() =>
      filteredTasks.value.filter(
          t => normalizarEstado(t) === "En progreso"
      )
  )

  const en_revision = computed(() =>
      filteredTasks.value.filter(
          t => normalizarEstado(t) === "En revisión"
      )
  )

  const completada = computed(() =>
    filteredTasks.value.filter(
        t => normalizarEstado(t) === "Completada"
    )
  )

  //FUNCION ACTUALIZAR FILTRO
  async function setFilters(newFilters){
    filters.value={
      ...filters.value,
      ...newFilters
    }

    const params = {}

    if (filters.value.proyecto) {
      params.proyecto = filters.value.proyecto
    }

    if (filters.value.estado) {
      params.estado = filters.value.estado
    }

    if (filters.value.prioridad) {
      params.prioridad = filters.value.prioridad
    }

    await obtenerTareas(params)
  }

  // Obtener todas las tareas
  async function obtenerTareas(params={}) {
    try{
      const res = await taskService.getAll(params)

      tareas.value = Array.isArray(res.data) ? res.data : []
    } finally{
      // this.loading=false
    }

  }

  // Obtener una tarea
  async function obtenerTarea(id) {
    try {
      const res = await taskService.getById(id)
      tareaActual.value = res.data
    } finally {
      // this.loading = false
    }
  }

  // Crear tarea
  async function crearTarea(data) {
    const payload = {

      titulo: data.titulo,
      descripcion: data.descripcion,
      proyecto: data.proyecto,
      estado: data.estado,
      prioridad: data.prioridad,
      fecha_limite: data.fecha_limite

    }

    if(data.esfuerzo_estimado){
      payload.esfuerzo_estimado = data.esfuerzo_estimado

    }

    const res = await taskService.create(payload)

    const completa = await taskService.getById(res.data.id)

    tareas.value.push(completa.data)
    return completa.data

  }

  // Actualizar tarea
  async function actualizarTarea(id, data) {

    await taskService.patch(id, data)

    const actualizada = await taskService.getById(id)

    const index = tareas.value.findIndex(
      t => t.id === id
    )

    if(index !== -1){
        tareas.value[index] = actualizada.data
    }

    tareaActual.value = actualizada.data

    return actualizada.data
}

  // Actualizar parcialmente
  async function actualizarParcial(id, data) {

      await taskService.patch(id, data)

      const completa = await taskService.getById(id)

      const index = tareas.value.findIndex(t => t.id === id)

      if (index !== -1) {
          tareas.value[index] = completa.data
      }

      tareaActual.value = completa.data

      return completa.data
  }

  // Eliminar
  async function eliminarTarea(id) {

    await taskService.remove(id)
    tareas.value = tareas.value.filter(
      t => t.id !== id
    )
  }

  return{
    tareas,
    tareaActual,
    filters,
    filteredTasks,
    pendiente,
    progreso,
    en_revision,
    completada,
    setFilters,
    obtenerTareas,
    obtenerTarea,
    crearTarea,
    actualizarTarea,
    actualizarParcial,
    eliminarTarea
  }
})

