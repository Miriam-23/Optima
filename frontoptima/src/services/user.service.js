import api from './api'

export default {

    getAll() {
        return api.get('/api/users/')
    },

    getById(id) {
        return api.get(`/api/users/${id}/`)
    }

}