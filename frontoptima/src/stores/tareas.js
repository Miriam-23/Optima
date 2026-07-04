import { defineStore } from 'pinia'

export const useTareasStore = defineStore('tareas', {
  state: () => ({
    tareas: [
      {
        id: 1,
        titulo: 'Diseñar login',
        descripcion: 'UI moderna',
        estado: 'Por hacer',
        prioridad: 'Alta',
        proyectoId: 1,
      },
      {
        id: 2,
        titulo: 'Dashboard KPIs',
        descripcion: 'Métricas principales',
        estado: 'En Progreso',
        prioridad: 'Media',
        proyectoId: 1,
      },
      {
        id: 3,
        titulo: 'API proyectos',
        descripcion: 'Conectar backend',
        estado: 'Finalizada',
        prioridad: 'Alta',
        proyectoId: 2,
      },
    ],
  }),

  getters: {
    porProyecto: (state) => (proyectoId) =>
      state.tareas.filter(t => t.proyectoId === proyectoId),

    todo: (state) => state.tareas.filter(t => t.estado === 'Por hacer'),
    doing: (state) => state.tareas.filter(t => t.estado === 'En progreso'),
    done: (state) => state.tareas.filter(t => t.estado === 'Finalizada'),

    total: (state) => state.tareas.length,
  },

  actions: {
    agregarTarea(tarea) {
      this.tareas.push({
        id: Date.now(),
        ...tarea,
      })
    },

    cambiarEstado(id, estado) {
      const t = this.tareas.find(x => x.id === id)
      if (t) t.estado = estado
    },
  },
})