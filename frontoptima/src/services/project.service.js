import api from './api'

export default {

  getAll() {
    return api.get('/projects/')
  },

  getById(id) {
    return api.get(`/projects/${id}/`)
  },

  // Endpoint maestro para el Dashboard Operativo del proyecto
  getDashboard(id) {
    return api.get(`/projects/${id}/dashboard/`)
  },

  create(data) {
    return api.post('/projects/', data)
  },

  update(id, data) {
    return api.put(`/projects/${id}/`, data)
  },

  patch(id, data) {
    return api.patch(`/projects/${id}/`, data)
  },

  remove(id) {
    return api.delete(`/projects/${id}/`)
  }

}