import api from './api'

export default {

  // ==========================================
  // LISTAR COMENTARIOS
  // GET /api/comments/
  // ==========================================
  getAll(params = {}) {
    return api.get('/api/comments/', { params })
  },

  // ==========================================
  // COMENTARIOS POR TAREA
  // GET /api/comments/?tarea=5
  // ==========================================
  getByTask(taskId) {
    return api.get('/api/comments/', {
      params: {
        tarea: taskId
      }
    })
  },

  // ==========================================
  // CREAR COMENTARIO
  // POST /api/comments/
  // ==========================================
  create(data) {
    return api.post('/api/comments/', data)
  },

  // ==========================================
  // ELIMINAR COMENTARIO
  // DELETE /api/comments/{id}/
  // ==========================================
  delete(id) {
    return api.delete(`/api/comments/${id}/`)
  }

}