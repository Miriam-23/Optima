import api from './api'

export default {

    getAll() {
        return api.get('/api/roles/')
    },

    getById(id) {
        return api.get(`/api/roles/${id}/`)
    }

}