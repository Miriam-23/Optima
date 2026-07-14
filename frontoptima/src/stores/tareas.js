import { defineStore } from 'pinia'
import taskService from '@/services/task.service'

export const useTareasStore = defineStore('tareas', {
  state: () => ({
    tareas: [],
    tareaActual: null,
    loading: false,
    error: null
  }),

  getters: {
    // porProyecto: (state) => (proyectoId) =>
    //   state.tareas.filter(t => t.proyectoId === proyectoId),
    porProyecto: (state) => (proyectoId) =>
      state.tareas.filter(t => t.proyecto === proyectoId),

    pendiente: (state) => state.tareas.filter(t => t.nombre_estado === 'Por hacer'),
    progreso: (state) => state.tareas.filter(t => t.nombre_estado === 'En progreso'),    
    revision: (state) => state.tareas.filter(t => t.nombre_estado === 'En revision'),
    completado: (state) => state.tareas.filter(t => t.nombre_estado === 'Completado'),
    total: (state) => state.tareas.length,
  },

  actions: {
    // Obtener todas las tareas
    async obtenerTareas() {
      this.loading = true
      try {
        const res = await taskService.getAll()
        console.log(res.data)
        this.tareas = res.data
      } catch (error) {
        console.log(error)
        this.error = error.res?.data || error.message
      } finally {
        this.loading = false
      }
    },

    // Obtener una tarea
    async obtenerTarea(id) {
      this.loading = true

      try {
        const res = await taskService.getById(id)
        this.tareaActual = res.data
      } finally {
        this.loading = false
      }
    },

    // Crear tarea
    async crearTarea(data) {

      const res = await taskService.create(data)
      this.tareas.push(res.data)
      return res.data
    },

    // Actualizar tarea
    async actualizarTarea(id, data) {

      const res = await taskService.update(id, data)
      const index = this.tareas.findIndex(t => t.id === id)

      if (index !== -1) {
        this.tareas[index] = res.data
      }

      this.tareaActual = res.data
      return res.data
    },

    // Actualizar parcialmente
    async actualizarParcial(id, data) {

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
    },

    // Eliminar
    async eliminarTarea(id) {

      await taskService.remove(id)
      this.tareas = this.tareas.filter(
        t => t.id !== id
      )
    }

  },
})