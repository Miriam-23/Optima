import api from './api'

export default {

  // ==========================================
  // LISTAR COMENTARIOS
  // GET /api/comments/
  // ==========================================
  getAll(params = {}) {
    return api.get('/comments/', { params })
  },

  // ==========================================
  // COMENTARIOS POR TAREA
  // GET /api/comments/?tarea=5
  // ==========================================
  getByTask(taskId) {
    return api.get('/comments/', {
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
    return api.post('/comments/', data)
  },

  // ==========================================
  // ELIMINAR COMENTARIO
  // DELETE /api/comments/{id}/
  // ==========================================
  delete(id) {
    return api.delete(`/comments/${id}/`)
  }

}