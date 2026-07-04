import api from './api'

export default {

  getAll() {
    return api.get('/api/projects/')
  },

  getById(id) {
    return api.get(`/api/projects/${id}/`)
  },

  create(data) {
    return api.post('/api/projects/', data)
  },

  update(id, data) {
    return api.put(`/api/projects/${id}/`, data)
  },

  patch(id, data) {
    return api.patch(`/api/projects/${id}/`, data)
  },

  remove(id) {
    return api.delete(`/api/projects/${id}/`)
  }

}