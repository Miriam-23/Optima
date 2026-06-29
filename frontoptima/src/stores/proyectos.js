import { defineStore } from 'pinia'

export const useProyectosStore = defineStore('proyectos', {
  state: () => ({
    proyectos: [
      {
        id: 1,
        nombre: 'Sistema Web OptimaPM',
        descripcion: 'Gestor de proyectos interno',
        estado: 'activo',
      },
      {
        id: 2,
        nombre: 'App Mobile Recycle',
        descripcion: 'App ecológica',
        estado: 'pausado',
      },
    ],
  }),

  getters: {
    total: (state) => state.proyectos.length,

    activos: (state) =>
      state.proyectos.filter(p => p.estado === 'activo'),

    pausados: (state) =>
      state.proyectos.filter(p => p.estado === 'pausado'),
  },

  actions: {
    agregarProyecto(proyecto) {
      this.proyectos.push({
        id: Date.now(),
        ...proyecto,
      })
    },

    eliminarProyecto(id) {
      this.proyectos = this.proyectos.filter(p => p.id !== id)
    },

    actualizarProyecto(id, data) {
      const index = this.proyectos.findIndex(p => p.id === id)
      if (index !== -1) {
        this.proyectos[index] = { ...this.proyectos[index], ...data }
      }
    },
  },
})