import api from './api'

export default {

  // Obtener todas las tareas
  getAll() {
    return api.get('/api/tasks/')
  },

  // Obtener las tareas de un proyecto
  getByProject(projectId) {
    return api.get(`/api/tasks/?project=${projectId}`)
  },

  // Obtener una tarea
  getById(id) {
    return api.get(`/api/tasks/${id}/`)
  },

  // Crear tarea
  create(data) {
    return api.post('/api/tasks/', data)
  },

  // Actualizar completamente
  update(id, data) {
    return api.put(`/api/tasks/${id}/`, data)
  },

  // Actualizar parcialmente
  patch(id, data) {
    return api.patch(`/api/tasks/${id}/`, data)
  },

  // Eliminar
  remove(id) {
    return api.delete(`/api/tasks/${id}/`)
  }

}
