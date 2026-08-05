import api from './api'

export default {
  getGlobales() {
    return api.get('/reports/')
  }
}