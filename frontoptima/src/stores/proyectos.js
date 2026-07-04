import { defineStore } from 'pinia'
import projectService from '@/services/project.service'

export const useProyectosStore = defineStore('proyectos', {
  state: () => ({
    proyectos: [],
    loading: false,
    error: null
  }),
  getters: {

    total: (state) => state.proyectos.length,

    activos: (state) =>
      state.proyectos.filter(p => p.estado_general === 'Planificacion'),

    activos: (state) =>
    state.proyectos.filter( p => p.estado_general === 'En progreso'),

    pausados: (state) =>
    state.proyectos.filter( p => p.estado_general === 'Pausado'),

    completado: (state) =>
    state.proyectos.filter( p => p.estado_general === 'Completado'),

  },
  actions: {

    async obtenerProyectos() {
      this.loading = true

      try {
        const response = await projectService.getAll()

        console.log(response.data)

        this.proyectos = response.data

      } catch (error) {
        console.log(error)
        this.error = error.response?.data || error.message
      } finally {
        this.loading = false
      }
    },

    async crearProyecto(data){
      const response = await projectService.create(data)
      console.log("Proyecto creado:", response.data)
      this.proyectos.push(response.data)
    },

    async actualizarProyecto(id,data){
      const response = await projectService.update(id,data)
      const index = this.proyectos.findIndex(p=>p.id===id)

      if(index!=-1){
        this.proyectos[index]=response.data
      }
    },

    async eliminarProyecto(id){
      await projectService.remove(id)
      this.proyectos=this.proyectos.filter(p=>p.id!==id)
    }
  },
})