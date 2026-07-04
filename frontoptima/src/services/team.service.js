import api from './api'

export default {

    getAll() {
        return api.get('/api/team/')
    },

    getById(id) {
        return api.get(`/api/team/${id}/`)
    },

    create(data) {
        return api.post('/api/team/', data)
    },

    remove(id) {
        return api.delete(`/api/team/${id}/`)
    }

}