import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import taskService from '@/services/task.service'

export const useTareasStore = defineStore('tareas', () => {

  const tareas = ref([])
  const filters = ref({
    search:'',
    proyecto:null,
    estado:null,
    prioridad:null
  })

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
        filters.value.proyecto &&
        task.proyecto===filters.value.proyecto
      ){
        } else if(filters.value.proyecto){
          return false
        }
        if(
          filters.value.estado &&
          task.nombre_estado!==filters.value.estado
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
  const pendiente = computed(()=>
    filteredTasks.value.filter(
      t=>t.nombre_estado==="Por hacer"
    )
  )

  const progreso = computed(()=>
    filteredTasks.value.filter(
      t=>t.nombre_estado==="En progreso"
    )
  )

  const revision = computed(()=>
    filteredTasks.value.filter(
      t=>t.nombre_estado==="En revision"
    )
  )

  const completado = computed(()=>
    filteredTasks.value.filter(
      t=>t.nombre_estado==="Completado"
    )
  )

  //FUNCION ACTUALIZAR FILTRO
  function setFilters(newFilters){
    filters.value={
      ...filters.value,
      ...newFilters
    }
  }
  // Obtener todas las tareas
  async function obtenerTareas(params={}) {
    // this.loading=true

    try{
      const res = await taskService.getAll(params)
      tareas.value = res.data
    } finally{
      // this.loading=false
    }

  }

  // Obtener una tarea
  async function obtenerTarea(id) {
    // this.loading = true

    try {
      const res = await taskService.getById(id)
      this.tareaActual = res.data
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
    this.tareas.push(res.data)
    return res.data

  }

  // Actualizar tarea
  async function actualizarTarea(id, data) {

    const res = await taskService.update(id, data)
    const index = this.tareas.findIndex(t => t.id === id)

    if (index !== -1) {
      this.tareas[index] = res.data
    }

    this.tareaActual = res.data
    return res.data
  }

  // Actualizar parcialmente
  async function actualizarParcial(id, data) {

    const res = await taskService.patch(id, data)
    const index = this.tareas.findIndex(t => t.id === id)

    if (index !== -1) {
      this.tareas[index] = {
        ...this.tareas[index],
        ...res.data
      }
    }

    this.tareaActual = res.data
    return res.data
  }

  // Eliminar
  async function eliminarTarea(id) {

    await taskService.remove(id)
    this.tareas = this.tareas.filter(
      t => t.id !== id
    )
  }

  return{
    tareas,
    filters,
    filteredTasks,
    pendiente,
    progreso,
    revision,
    completado,
    setFilters,
    obtenerTareas,
    crearTarea,
    actualizarTarea,
    eliminarTarea
  }
})

