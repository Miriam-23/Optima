import api from './api'
export default {

  // ==========================================
  // LISTAR ASIGNACIONES
  // ==========================================
  getAll(params = {}) {
    return api.get('/api/assignments/', { params })
  },

  // ==========================================
  // ASIGNAR USUARIO A TAREA
  // ==========================================
  create(data) {
    return api.post('/api/assignments/', data)
  },

  // ==========================================
  // ELIMINAR ASIGNACIÓN
  // ==========================================
  delete(id) {
    return api.delete(`/api/assignments/${id}/`)
  }

}