import api from './api'

export default {

  // ==========================================
  // LISTAR ESTADOS
  // GET /api/statuses/
  // ==========================================
  getAll() {
    return api.get('/api/statuses/')
  },

  // ==========================================
  // DETALLE DE ESTADO
  // GET /api/statuses/{id}/
  // ==========================================
  getById(id) {
    return api.get(`/api/statuses/${id}/`)
  }

}