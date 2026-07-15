import api from './api'

export default {
  getAll() {
    return api.get('/api/notifications/')
  },

  markAllAsRead() {
    return api.post('/api/notifications/marcar-leidas/')
  }
}
