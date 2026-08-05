import api from './api'

export default {
  getAll() {
    return api.get('/notifications/')
  },

  markAllAsRead() {
    return api.post('/notifications/marcar-leidas/')
  }
}
