import api from './api'

export default {

  // Obtener todas las tareas
  getAll(params = {}) {
    return api.get('/tasks/', { params })
  },

  // Obtener las tareas de un proyecto
  getByProject(projectId) {
    return api.get(`/tasks/?project=${projectId}`)
  },

  // Obtener una tarea
  getById(id) {
    return api.get(`/tasks/${id}/`)
  },

  // Crear tarea
  create(data) {
    return api.post('tasks/', data)
  },

  // Actualizar completamente
  update(id, data) {
    return api.put(`/tasks/${id}/`, data)
  },

  // Actualizar parcialmente
  patch(id, data) {
    return api.patch(`/tasks/${id}/`, data)
  },

  // Eliminar
  remove(id) {
    return api.delete(`/tasks/${id}/`)
  }

}
